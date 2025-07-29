# Examples

To run the examples either ensure the development dependencies have been installed (see [installation](installation.md)) or, if you are working from the project's git repository, be sure to enter the correct `hatch` environment. For example, from the project root:

```bash
hatch shell
python examples/00-simple-decorator.py
```

## Display Global Interfaces
Using the decorator method of custom class registration.

```python
--8<-- "examples/00-simple-decorator.py"
```

## Display Global Interfaces
Using explicit custom class registration.

```python
--8<-- "examples/10-simple-explicit.py"
```

## List Available Monitors
Obtains and prints information about the available display outputs.

```python
--8<-- "examples/20-list-monitors.py"
```

## Top-Level Window
This example demonstrates everything required to create a top-level application window and manage memory pools and surface buffers. It simply displays the Wayland logo in window and resizes the logo as the window is resized.

It demonstrates the use of the [SharedMemoryPool][wayland.client.memory_pool] helper class to handle all of the low level memory allocation for the surface buffers.

It also demonstrates a number of other `python-wayland` features, including three different methods of implementing event handlers.

```python
--8<-- "examples/30-main-window.py"
```

The PNGImage class used in the example:

```python
--8<-- "examples/png.py"
```