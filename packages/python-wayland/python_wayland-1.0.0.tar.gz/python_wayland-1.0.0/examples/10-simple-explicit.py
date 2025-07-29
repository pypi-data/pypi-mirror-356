# examples/10-simple-explicit.py

# Print a list of Wayland global interfaces
import wayland
from wayland.client import register_factory


class Registry(wayland.wl_registry):

    def on_global(self, name, interface, version):
        print(f"{interface} (version {version})")


if __name__ == "__main__":

    register_factory("wl_registry", Registry)

    display = wayland.wl_display()
    registry = display.get_registry()

    while True:
        display.dispatch_timeout(0.2)
