# Installation

## Install Using `pip`

Installation of only what is required at runtime:

```bash
pip install python-wayland
```

Installation including dependencies required for running the examples and other development utils:

```bash
pip install python-wayland[dev]
```

## Install Using `uv`

```bash
uv add python-wayland

# With examples and dev tools

```
uv add python-wayland[dev]

## Requirements

* Python 3.8 or higher
* A Wayland compositor (for runtime use)

No additional dependencies outside of the standard Python library are mandatory at runtime. For development, testing and debugging, other Python packages are recommended and configured into the package configuration.

## Install Using `git`

If you want to use the `python-wayland` library it's easier to install as above. Clone the git repository if you want to change `python-wayland` itself or want access to the latest development version.

```bash
git clone https://git.sr.ht/~gk/python-wayland
```

Be sure to read the [quickstart notes](developing-quickstart.md) if you're working from the project's git repository.