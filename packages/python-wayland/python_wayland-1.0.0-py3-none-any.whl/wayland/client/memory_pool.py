# Copyright (c) 2024-2025 Graham R King
# Licensed under the MIT License. See LICENSE file for details.

from __future__ import annotations

import contextlib
import ctypes
import mmap
import os
import tempfile

import wayland
from wayland.log import log


class SharedMemoryPoolError(Exception):
    """Exception for SharedMemoryPool errors."""


class SharedMemoryPool:
    """
    A helper that provides a simple method of managing surface
    memory pools and buffers.

    Simply call create_buffer(width, height) any time a buffer is required for
    updating a surface. A [wayland.wl_buffer][] instance and a pointer to the
    buffer are returned. This class handles everything else, double
    buffering (quad-buffering by default in fact), pool resizing, etc.

    See `examples/30-main-window.py` for an example using SharedMemoryPool
    to display a main application window surface.

    """

    def __init__(self, shm: wayland.wl_shm):
        """
        Initialize the SharedMemoryPool.

        Args:
            shm: Wayland shared memory object.
        """
        # Public properties
        self.bytes_per_pixel = 4  # matches the default argb8888
        self.number_of_buffers = 4  # quad buffering
        self.hysteresis_threshold = 0.1  # 10% change required for recreation
        # Recreate if current pool > threshold times requested
        self.waste_threshold = 5.5
        self.force_release_frames = 3  # Force release buffers after 3 frames

        self._shm = shm
        self._fd = None
        self._pool_data = None  # uint8 pointer to pool data
        self._pool_size = 0
        self._buffer_size = 0
        self._num_buffers = self.number_of_buffers
        self._wl_shm_pool = None
        self._mapped_file = None
        self._buffers: list[wayland.wl_buffer | None] = [None] * self._num_buffers
        self._buffer_states = [False] * self._num_buffers  # Track release state
        self._buffer_frame_count = [
            0
        ] * self._num_buffers  # Track frames since buffer was used
        self._frame_counter = 0

        # Dynamic pool management state
        self._current_pool_width = 0
        self._current_pool_height = 0
        self._pool_recreation_count = 0

    def create_buffer(
        self,
        width: int,
        height: int,
        pixel_format: wayland.wl_shm.format = wayland.wl_shm.format.argb8888,
    ) -> tuple[wayland.wl_buffer, ctypes.POINTER[ctypes.c_uint8]] | tuple[None, None]:  # type: ignore
        """
        Get a pointer to a buffer, creating it if necessary.

        The buffer pointer returned is cast to `ctypes.c_uint8` (unsigned byte),
        it is suitable for directly writing into, either from Python or with
        an external library, such as cv2, pillow, etc.

        Args:
            width: Width of the buffer in pixels
            height: Height of the buffer in pixels
            pixel_format: The pixel format of the surface.

        Returns:
            Tuple containing the buffer and its pointer
        """
        if not self._recreate_pool_if_needed(width, height):
            log.debug("Failed to recreate pool on demand")
            return None, None

        self._frame_counter += 1
        self._force_release_stale_buffers()

        buffer_number = self._find_available_buffer_slot()
        if buffer_number == -1:
            log.warning("No free buffer slots found. States: %s", self._buffer_states)
            return None, None

        self._cleanup_old_buffer(buffer_number)
        offset = self._validate_buffer_offset(buffer_number)

        buffer = self._create_wayland_buffer(offset, width, height, pixel_format)
        self._setup_buffer_tracking(buffer_number, buffer)
        ptr = self._create_buffer_pointer(offset)

        log.debug("Returning buffer and ptr")
        if buffer and ptr:
            return buffer, ptr
        return None, None

    def _force_release_stale_buffers(self):
        """Mark buffers as available if they haven't been released after configured frames."""
        for i in range(len(self._buffer_states)):
            if (
                not self._buffer_states[i]
                and self._buffers[i] is not None
                and self._frame_counter - self._buffer_frame_count[i]
                >= self.force_release_frames
            ):
                frame_diff = self._frame_counter - self._buffer_frame_count[i]
                log.debug("Force-releasing buffer %s after %s frames", i, frame_diff)
                self._buffer_states[i] = True

    def _find_available_buffer_slot(self) -> int:
        """Find an available buffer slot, returning -1 if none found."""
        log.debug(f"Buffers: {self._buffers}")
        for i, (buf, released) in enumerate(zip(self._buffers, self._buffer_states)):
            if buf is None or released:
                return i
        return -1

    def _cleanup_old_buffer(self, buffer_number: int):
        """Clean up old buffer if reusing a released slot."""
        buffer = self._buffers[buffer_number]
        if buffer and self._buffer_states[buffer_number]:
            with contextlib.suppress(Exception):
                buffer.destroy()
            self._buffers[buffer_number] = None

    def _validate_buffer_offset(self, buffer_number: int) -> int:
        """Validate buffer offset and return it."""
        offset = self._buffer_size * buffer_number
        if offset + self._buffer_size > self._pool_size:
            msg = f"Buffer offset {offset} exceeds pool size {self._pool_size}"
            raise SharedMemoryPoolError(msg)
        return offset

    def _create_wayland_buffer(
        self, offset: int, width: int, height: int, pixel_format
    ) -> wayland.wl_buffer | None:
        """Create the Wayland buffer object."""
        if not self._wl_shm_pool:
            return None
        return self._wl_shm_pool.create_buffer(
            offset, width, height, width * self.bytes_per_pixel, pixel_format
        )

    def _setup_buffer_tracking(
        self, buffer_number: int, buffer: wayland.wl_buffer | None
    ):
        """Set up buffer tracking and release callback."""
        if not buffer:
            return

        log.debug(f"Saved to buffer number {buffer_number}")
        self._buffers[buffer_number] = buffer
        self._buffer_states[buffer_number] = False
        self._buffer_frame_count[buffer_number] = self._frame_counter

        try:
            # Wayland release events don't pass parameters, so we need to capture buffer_number
            def release_callback():
                self._on_release_buffer(buffer_number)

            buffer.events.release += release_callback  # type: ignore[operator,method-assign]
        except Exception as e:
            log.exception("Failed to set release callback")
            msg = f"Failed to set release callback: {e}"
            raise SharedMemoryPoolError(msg) from e

    def _create_buffer_pointer(
        self, offset: int
    ) -> ctypes.POINTER[ctypes.c_uint8] | None:  # type: ignore
        """Create and return buffer pointer."""
        if not self._pool_data:
            return None

        try:
            base_addr = ctypes.addressof(self._pool_data.contents)
            target_addr = base_addr + offset
            return ctypes.cast(target_addr, ctypes.POINTER(ctypes.c_uint8))
        except Exception as e:
            msg = f"Failed to create buffer pointer: {e}"
            raise SharedMemoryPoolError(msg) from e

    def _create_pool(self, width=0, height=0, num_buffers=None):
        """
        Create a memory pool based on given dimensions and number of buffers.
        """
        if self._fd:
            msg = "Attempt to create pool that already exists"
            raise SharedMemoryPoolError(msg)

        if num_buffers is None:
            num_buffers = self.number_of_buffers

        # Calculate required memory size
        self._num_buffers = num_buffers
        self._buffer_size = width * height * self.bytes_per_pixel
        self._pool_size = self._buffer_size * num_buffers

        # Create and truncate temporary file to match pool size
        self._fd, _ = tempfile.mkstemp()
        os.ftruncate(self._fd, self._pool_size)

        # Memory-map the file
        self._mapped_file = mmap.mmap(
            self._fd, self._pool_size, access=mmap.ACCESS_WRITE
        )

        # Create pool data pointer
        self._pool_data = ctypes.cast(
            ctypes.addressof(ctypes.c_uint8.from_buffer(self._mapped_file)),
            ctypes.POINTER(ctypes.c_uint8),
        )

        # Create the Wayland shared memory pool
        self._wl_shm_pool = self._shm.create_pool(self._fd, self._pool_size)

        # Initialize buffer slots and states
        self._buffers: list[wayland.wl_buffer | None] = [None] * num_buffers
        self._buffer_states = [False] * num_buffers  # False = not released
        self._buffer_frame_count = [0] * num_buffers

        # Track pool dimensions for dynamic management
        self._current_pool_width = width
        self._current_pool_height = height

    def _destroy_pool(self):
        """Destroy the current pool and release resources."""
        if not self._fd:
            return

        # Destroy all buffers before touching shm
        for i, buffer in enumerate(self._buffers):
            if buffer and not self._buffer_states[i]:  # Only destroy if not released
                with contextlib.suppress(Exception):
                    buffer.destroy()
                self._buffers[i] = None

        # Destroy the pool
        if self._wl_shm_pool:
            with contextlib.suppress(Exception):
                self._wl_shm_pool.destroy()
            self._wl_shm_pool = None

        # Clean up memory mapping
        if self._mapped_file:
            self._mapped_file.close()
            self._mapped_file = None

        if self._fd:
            os.close(self._fd)
            self._fd = None

        self._buffers = []
        self._buffer_states = []
        self._buffer_frame_count = []
        self._frame_counter = 0
        self._pool_data = None

        # Reset dynamic pool tracking
        self._current_pool_width = 0
        self._current_pool_height = 0

    def _on_release_buffer(self, buffer_number):
        """
        Callback function when compositor releases a buffer.
        DON'T destroy here - just mark as released.

        :param buffer_number: Index of buffer to release
        """
        log.debug("Buffer %s released by compositor", buffer_number)
        if 0 <= buffer_number < len(self._buffer_states):
            self._buffer_states[buffer_number] = True

    def _should_recreate_pool(self, request_width, request_height):
        """Determine if pool needs recreation based on size requirements."""
        if not self._fd:
            log.debug("No pool file descriptor so needs to be recreated")
            return True

        request_size = request_width * request_height
        current_capacity = self._current_pool_width * self._current_pool_height
        log.debug(
            f"Request size {request_width}x{request_height} Current capacity {self._current_pool_width}x{self._current_pool_height}"
        )

        if (
            request_width > self._current_pool_width
            or request_height > self._current_pool_height
        ):
            return True

        if current_capacity > request_size * self.waste_threshold:
            log.debug("Current pool is too large.")
            return True

        if current_capacity > 0:
            size_change_ratio = abs(current_capacity - request_size) / current_capacity
            if size_change_ratio < self.hysteresis_threshold:
                return False

        return False

    def _calculate_optimal_pool_size(self, request_width, request_height):
        """Calculate optimal pool dimensions for given request."""
        # Add 25% growth buffer
        optimal_width = int(request_width * 1.25)
        optimal_height = int(request_height * 1.25)

        # Round to 64-pixel boundaries for cache efficiency
        optimal_width = ((optimal_width + 63) // 64) * 64
        optimal_height = ((optimal_height + 63) // 64) * 64

        # XXX: Assumes generally large surfaces
        optimal_width = max(1024, min(optimal_width, 16384))
        optimal_height = max(1024, min(optimal_height, 16384))

        return optimal_width, optimal_height

    def _recreate_pool_if_needed(self, width, height):
        """Recreate pool if current pool is inadequate."""
        if not self._should_recreate_pool(width, height):
            return True
        log.debug("Determined that the shm pool should be recreated")

        optimal_width, optimal_height = self._calculate_optimal_pool_size(width, height)

        log.debug(
            "Recreating buffer pool: %sx%s -> %sx%s",
            self._current_pool_width,
            self._current_pool_height,
            optimal_width,
            optimal_height,
        )

        old_num_buffers = self._num_buffers
        self._destroy_pool()

        try:
            self._create_pool(optimal_width, optimal_height, old_num_buffers)
        except SharedMemoryPoolError as e:
            log.warning("Failed to create optimal pool, trying smaller: %s", e)
            try:
                self._create_pool(width, height, old_num_buffers)
            except SharedMemoryPoolError:
                log.exception("Failed to create any buffer pool")
                return False
            else:
                return True
        else:
            self._pool_recreation_count += 1
            return True

    def __del__(self):
        """Destructor to ensure cleanup."""
        with contextlib.suppress(Exception):
            self._destroy_pool()
