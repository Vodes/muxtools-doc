## Muxing
All of your muxing needs right here.

Here I should maybe also mention the available "tokens" you can use for the filename and mkv title templates in your `Setup`.

### Tokens
- `$show$`<br>
    The show name. Taken from the current `Setup`.
- `$ep$`<br>
    The episode number/string. Taken from the current `Setup`.
- `$crc32$`<br>
    Used to generate a crc32 for the resulting mux.<br>
    You should probably not use this for the mkv title as setting mkv metadata will change the crc.
- `$title$`<br>
    Token for the episode title. This will only work if you use the [TMDB](#tmdb) integration.
- `$title_sanitized$`<br>
    Same as above but with the *title_sanitization* param in [TMDBConfig](/muxtools/muxing/tmdb/#muxtools.muxing.tmdb.TmdbConfig) applied to the string. 

You can also use *any* variable that's declared in Setup as a token.<br>
This also includes *any* "unknown" ones that you might have configured in the ini file.

For example: If you have a `group_name` variable in the ini or set via [Setup.edit](https://muxtools.vodes.pw/muxtools/main/#muxtools.main.Setup.edit) you can just use `$group_name$` as a token in filenames or titles.

### Basic Usage

This assumes you have the variables created in the previous 3 wiki entries. ([Encodes](/guide/encode-video), [Audio](/guide/encode-audio), [Subs & Chapters](/guide/subtitles-and-chapters))

```py
from vsmuxtools import Setup, mux

setup = Setup("01")

mux(
    video_hevc.to_track(name="Vodes Encode", lang="jpn", default=True),
    audio.to_track("Japanese 2.0 (Amazon)", "jpn", True),
    subtitle.to_track("English (CR)", "en", True),
    *fonts, # The * is necessary to unpack the list into multiple "tracks"
    chapters
)
# Note that this just returns the Path of the resulting mux. You can do whatever you feel like with it.
```

## TMDB

This package has a TMDB Integration so you can have episode titles and other [various metadata](/muxtools/muxing/tmdb/#muxtools.muxing.tmdb.TmdbConfig) in your mux.

```py
from vsmuxtools import mux, TitleTMDB, TmdbConfig, TMDBOrder

# This is useful for if you don't really care about any of the other metadata besides the ep title.
mux(..., tmdb=TitleTMDB(117465))

# Otherwise you can have fun with every option using this
mux(..., tmdb=TmdbConfig(117465, write_date=True, write_ids=True, write_summary=True))

# You can also use episode groups/orders via their ID
# This for example selects the *proper* season 2 for jujutsu kaisen.
mux(..., tmdb=TmdbConfig(95479, 2, order="64a3fc4fe9da6900ae2fa807"))

# or auto-select an them using the enum
# Automatically fetches the same ID as the example right above this.
mux(..., tmdb=TmdbConfig(95479, 2, order=TMDBOrder.PRODUCTION))
```