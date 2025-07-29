# We use opencv to handle the PNG image for this example
# pip install opencv-python
import ctypes
import os
import cv2

class PngImage:
   """Simple PNG image loader."""

   def __init__(self):
       self.src_image = None
       self.current_image = None
       self.current_width = 0
       self.current_height = 0

   def load_png(self, filename):
       script_dir = os.path.dirname(os.path.abspath(__file__))
       full_path = os.path.join(script_dir, filename)

       self.src_image = cv2.imread(full_path, cv2.IMREAD_UNCHANGED)

       # Ensure we have 4 channels (BGRA)
       while self.src_image.shape[2] < 4:
           self.src_image = cv2.cvtColor(self.src_image, cv2.COLOR_BGR2BGRA)

       self.current_image = self.src_image
       self.current_height, self.current_width = self.src_image.shape[:2]
       return True

   def copy_to_buffer(self, buffer, width, height):
       # Only resize if current image isn't the right size
       if self.current_width != width or self.current_height != height:
           self.current_image = cv2.resize(self.src_image, (width, height))
           self.current_width, self.current_height = width, height

       # Copy BGRA data directly (matches little-endian ARGB8888)
       pixels = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint32))
       ctypes.memmove(pixels, self.current_image.tobytes(), width * height * 4)
       return True
