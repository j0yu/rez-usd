# USD

[![CI](../..//workflows/CI/badge.svg?branch=master)](../../actions?query=workflow%3ACI+branch%3Amaster)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


[rez] package to install [USD].

Here are some beginners instructions on how to use this repository.

## Installation

1. Install [rez] via `python install.py` method
1. Clone/download this repository
1. Ensure at least the folder printed by
   this command `rez config local_packages_path`
1. Open terminal in (extracted) repository folder,
   run `rez build --install`

USD should now be installed as a [rez] package named `usd`.

- [shbang] of [Python USD Tools] replaced with `env python*.*` calls
- Has a copy of [aswf/ci-usd]'s `lib` and `lib64` libraries from `/usr/local`.

## Usage

To run [USD]: `rez env usd -- usdcat --help`

You'll also need PySide/PySide2 and PyOpenGL if you want to use `usdview`

```bash
rez pip --install PySide2
rez pip --install PyOpenGL
rez env usd PySide2 PyOpenGL -- usdview path/to/scene.usd
```

## Maintenance

Whenever new official release come out, update the `__version__`
in `package.py` then re-run `rez build --install`.

If you decide to make another install, e.g. new `commands()` environment
setup, you can instead just update the `+local.` version number to indicate
new releases/versions of your own. See [PEP 540 local version segments].

Also, you can rename `+local.` to something more relevant to you 
e.g. `+mystudio.` or  `+mygithubname.`

----

Want more rez packages? Checkout [my GitHub repositories][j0yu-rez-packages]

[rez]: https://github.com/nerdvegas/rez
[requirement]: https://github.com/nerdvegas/rez/wiki/Package-Definition-Guide#requires
[j0yu-rez-packages]: https://github.com/j0yu?tab=repositories&q=topic%3Arez+topic%3Apackage
[USD]: https://github.com/PixarAnimationStudios/USD
[PEP 540 local version segments]: https://www.python.org/dev/peps/pep-0440/#local-version-segments
[aswf/ci-usd]: https://github.com/AcademySoftwareFoundation/aswf-docker/blob/master/ci-usd/Dockerfile#L55-L71
[shbang]: https://en.wikipedia.org/wiki/Shebang_(Unix)#Syntax
[Python USD Tools]: https://graphics.pixar.com/usd/docs/USD-Toolset.html