# Getting started
Some necessities used/needed for essentially every script<br>

## Setup

For detailed information on every parameter, check the [docs](/muxtools/main/#muxtools.main.Setup).

```py
from vsmuxtools import Setup

setup = Setup("01") # This is just the episode number
```

This is used for most if not all workflows in this package and should be set at the start of every script.<br>
Initially it will prompt you to fill out the generated `config.ini` file.<br>

This will create a work directory under `./_workdir/<episode you passed>`. Every function uses this as its default output.<br>
If you do decide to not use a Setup it will dump everything in your current directory.

## SRC_FILE

Simple convenience wrapper for sources.

```py
from vstools import core
from vsmuxtools import src_file # Other aliases for this are SRC_FILE and FileInfo

# force_lsmas simply uses lsmashsource if True and otherwise tries to use DGIndexNV
JPBD = src_file(R"F:\BDMV\Main Disc\BDMV\STREAM\00002.m2ts", force_lsmas=True)

# You can also set a initial trim, in this example it'll make the cut clip start at the 24th frame 
# and cut off 24 frames at the end
JPBD = src_file(R"F:\BDMV\Main Disc\BDMV\STREAM\00002.m2ts", trim=(24, -24))

# You can also just set a custom indexing function that takes a path and returns a videonode
JPBD = src_file(R"F:\BDMV\Main Disc\BDMV\STREAM\00002.m2ts", idx = lambda file: core.lsmas.LWLibavSource(file))


# This is the uncut/untrimmed clip
src = JPBD.src

# This is the clip with trims applied
src = JPBD.src_cut

# Same deal as above but now applying vstools.initialize_clip
# (which makes a 16 bit clip by default and sets a bunch of useful props)
src = JPBD.init()
src = JPBD.init_cut()

# If you need the AudioNode for this src_file you can also use these.
# This just indexes the audio using bestsource. You can pass a track num and any other args as you wish.
audio = JPBD.get_audio()
audio = JPBD.get_audio_trimmed() # same deal as src/init_cut ofc
```