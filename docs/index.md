# Home

A library for various muxing and automation tools for anything and everything fansubbing related.<br>
The guide here is essentially a glorified examples section but I heard it works well enough.

`muxtools` contains all functionality that's possible without having vapoursynth.<br>
`vsmuxtools` is the extension to it that adds some more functionality to some existing functions but also adds all video encoding stuff.<br>
It also exports everything from muxtools so you should ever only have to use/import vs-muxtools if you have vapoursynth.

## Installation

Git is always the most updated one obviously but I can't guarantee that everything is in a working state.<br>
vs-muxtools depends on muxtools so you should uninstall both and reinstall starting with muxtools if you need latest git.
```
pip install git+https://github.com/Jaded-Encoding-Thaumaturgy/muxtools.git
pip install git+https://github.com/Jaded-Encoding-Thaumaturgy/vs-muxtools.git
```
<br>
You can also grab the latest stable ish versions from pip.

muxtools <br>[![PyPI version](https://badge.fury.io/py/muxtools.svg)](https://badge.fury.io/py/muxtools)

vsmuxtools <br>[![PyPI version](https://badge.fury.io/py/vsmuxtools.svg)](https://badge.fury.io/py/vsmuxtools)