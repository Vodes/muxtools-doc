## Subtitles

Uh... there are a lot of subtitle processing functions in the [SubFile class](/muxtools/subtitle/sub/#muxtools.subtitle.sub.SubFile).<br>
It would probably take a lot of time to explain them here again so go read the docs.

### Basic Usage
```py
from vsmuxtools import SubFile, GJM_GANDHI_PRESET, GlobSearch, dummy_video

# Might be worth noting that none of this touches the original input file
# A copy to the work directory is always the first step
# You can simply chain everything like this as they all return the SubFile object again
subtitle = SubFile(R"test.ass") \
    .resample("random video.mkv") \
    .restyle(GJM_GANDHI_PRESET) \
    .merge("opening.ass", "opsync") \
    .clean_styles()

# Also possible to resample with a dummy video
# Might be worth noting that not specifying a video at all will always create a 1920x1080 dummy video
subtitle.resample(dummy_video(width=1920, height=1080))

# You can do a basic merge of more 2+ files like this
subtitle = SubFile([R"dialogue.ass", R"signs.ass"])

# ... or with a GlobSearch
subtitle = SubFile(GlobSearch("*_en.ass", allow_multiple=True, dir="./subs/english"))

# Finally you can collect fonts
fonts = subtitle.collect_fonts()
```

All of those `subtitle` variables are a `SubFile` object.<br>
To get the filepath you simply do `subtitle.file`.<br><br>

## Chapters

As usual, check the [docs](/muxtools/chapters) for all the available functions you can use in Chapters.

Note that this doesn't include the src_file part because it's not in *muxtools*.<br>
For that, check [this](https://github.com/Irrational-Encoding-Wizardry/vs-muxtools/blob/master/vsmuxtools/extension/chapters.py).

```py
from vsmuxtools import Chapters, src_file

# If you pass a src_file it will try parsing it from the BDMV playlists if it detects a BDMV file stucture
# ofc it will also account for the trims
JPBD = src_file(R"F:\BDMV\Main Disc\BDMV\STREAM\00002.m2ts", trim=(24, 500))
chapters = Chapters(JPBD)

# then you could set the names like
chapters.set_names(["Prologue", "Opening", "Part A", "Part B", "Ending"])

# You can also manually define chapters like this: (obviously frame numbers)
chapters = Chapters([(0, "Prologue"), (2110, "Opening"), (4268, "Episode"), (32981, "Ending")])

# You can easily save the chapters to a ogm file with this
# If you don't pass your own output path it will default to "current workdir/chapters.txt"
chapters.to_file()
```