# python-wayland

[![PyPI - Version](https://img.shields.io/pypi/v/python-wayland.svg)](https://pypi.org/project/python-wayland) [![builds.sr.ht status](https://builds.sr.ht/~gk/python-wayland.svg)](https://builds.sr.ht/~gk/python-wayland?) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-wayland.svg)](https://pypi.org/project/python-wayland) [![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://python-wayland.org)

An implementation of the Wayland protocol from scratch, with no external dependencies, just Python. Aimed at building clients rather than compositors.

## Features

* Includes support for all standard Wayland protocols and extensions from Hyprland and wlroots.
* No external dependencies, no other Wayland libraries are required. This is not a wrapper for libwayland.
* Maintains the original Wayland naming conventions to ensure Wayland API documentation remains relevant and easy to use.
* Supports updating protocol definitions from either the local system or the latest official protocol repositories. Latest versions of all protocol definitions are built-in.
* Supports code completion, type hinting and documentation for Wayland objects. _(tested in vscode and helix)_

## Documentation

For documentation on how to use `python-wayland` see the [online documentation](https://python-wayland.org)

## Thanks

Thanks to Philippe Gaultier, whose article [Wayland From Scratch](https://gaultier.github.io/blog/wayland_from_scratch.html) inspired this project.

Thanks also to Drew DeVault for his [freely available Wayland book](https://wayland-book.com/). This project would not have been developed if not for Drew's book.

Thanks to the [`mkdocstrings` project](https://github.com/mkdocstrings/mkdocstrings), not only for the `mkdocstrings` plugin to [MkDocs](https://www.mkdocs.org/) but also because the configuration of the `python-wayland` documentation is almost entirely copied from the excellent work done by the `mkdocstrings` project in [their own documentation](https://mkdocstrings.github.io/).