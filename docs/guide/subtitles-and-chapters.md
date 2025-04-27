## Subtitles

Uh... there are a lot of subtitle processing functions in the [SubFile class](/muxtools/subtitle/sub/#muxtools.subtitle.sub.SubFile).<br>
It would probably take a lot of time to explain them here again so go read the docs.

### Basic Usage
```py
from muxtools import SubFile, GJM_GANDHI_PRESET, GlobSearch, dummy_video

# Might be worth noting that none of this touches the original input file
# A copy to the work directory is always the first step
# You can simply chain everything like this as they all return the SubFile object again
subtitle = SubFile(R"test.ass") \
    .resample("random video.mkv") \
    .restyle(GJM_GANDHI_PRESET) \
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

#### Merging and shifting
Shifting and merging with syncs *should* be done with timestamps.<br>
You can pass a `timesource` to every function that works with frame <-> conversions.<br>
Subtitles specifically can also fetch a default from the `Setup`. [See docs](/muxtools/main/#muxtools.main.Setup.set_default_sub_timesource).

If you never set one in either the functions or the Setup it will assume FPS timestamps with `24000/1001` and a timescale that's the usual on MKV files.<br>
And also print a warning because you probably shouldn't be doing that.

```py
subtitle.merge(
    "./songs/OP.ass", 
    "opsync", # Syncpoint in your current subtitle object/file
    "sync", # Syncpoint in the OP file. If none given this will just be the first non-comment line (sorted by start time)
    timesource="./premux/01.mkv" # Where to take the timestamps & timescale from.
)
```

If you want to match SubKt in its merging with syncpoints behavior you need to set the `shift_mode` param.<br>
SubKt shifts by `TIME` directly without considering frames or a video file at all.<br>
You can see the available ones [in the docs](/muxtools/subtitle/basesub/#muxtools.subtitle.basesub.ShiftMode).

There's also a full SubKt project port in the [examples section](/examples/#adapting-a-subkt-project-to-muxtools).

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

The chapters take a `timesource` and `timescale` param aswell albeit defaulting to FPS timestamps without a warning.<br>
Using a `src_file` or doing `Chapters.from_mkv` will automatically fetch them from that respective video.

**Chapters will not fetch a default from the setup!**<br>
(unless you're doing `Chapters.from_sub`)

## Also notable

muxtools offers a CLI command for generating a VideoMeta json file.

This may be of interest to you if you want to have all the necessary timestamp information in your fansub git repo.<br>
Perhaps to then do merges on CI and whatnot.

The usage is literally just: 
```
muxtools gen-vm "path/to/your/video.mkv"
muxtools generate-videometa "video.mkv" "out.json"
```

Output being optional and, if not given, creating a `video_meta.json` file in your current directory with these samples.