# Muxing
All of your muxing needs right here.

Here I should maybe also mention the available "tokens" you can use for the filename and mkv title templates in your `Setup`.

## Tokens
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

## Dynamic metadata tokens

Starting with `0.4.1` you can use a couple of predetermined tokens for automatic replacements based on metadata.

| Token    | Meaning | Example | Ambiguous
| -------- | ------- | ---- | ---- |
| `$lang$`  | The language tag of a track as-is | `DE` | yes
| `$lang3$` | The language of a track in its alpha-3 form     | `DEU` | yes
| `$lang3b$`   | The language of a track in its [bibliographic](https://github.com/georgkrause/langcodes?tab=readme-ov-file#getting-alpha3-codes) alpha-3 form   | `GER`  | yes
| `$language$`   | The display name for the language of a track    | `German`  | yes
| `$format$` / `$codec$`   | The format name of a track | `Opus` / `HEVC`  | yes
| `$bits$` / `$depth$`   | The bitdepth of a *video* or *audio*  track | `10` / `24`  | yes
| `$res$` / `$resolution$`   | The height of a *video* track | `1080p`  | no
| `$ch$` / `$channels$`   | The channel layout of an *audio* track | `7.1` / `2.0`  | no

Any of these can be used in both tracks and `out_name` templates.<br>
***Not in the mkv title naming for now.***

For example: 
```py
Setup("01", None, out_name="Example - S01E$ep$ (BD $res$ $vformat$ $aformat$) [Dual-Audio] [Group]")

video = x264().encode(USBD.init_cut(10)).to_track("Test Enc $format$") # Results in "Test Enc H264"

jp = do_audio(USBD, 2).to_track("$language$ $ch$ (USBD)", "ja") # Results in "Japanese 2.0 (USBD)"
en = do_audio(USBD, 0).to_track("$language$ $ch$ (USBD)", "en") # Results in "English 5.1 (USBD)"
de = do_audio(DEBD, 0).to_track("$language$ $ch$ (DEBD)", "de") # Results in "German 2.0 (DEBD)"

mux(video, jp, en, de) # Results in "Example - S01E01 (BD 1080p H264 Opus) [Dual-Audio] [Group].mkv"
```
### Track selection
As you can see in the `out_name` example above, the tokens marked as *ambiguous* need to select a given track type or number when used in **filenames**.

Here are a few examples of how the selection can work:

| By type |  |
| ----- | ------- |
| `$vformat$` | The format of the first video track 
| `$aformat$` | The format of the first audio track
| `$sformat$` | The format of the first subtitle track

| By type with number |  |
| ----- | ------- |
| `$aformat_1$` | The format of the **second** audio track
| `$sformat_2$` | The format of the **third** subtitle track

| By type & language |  |
| ----- | ------- |
| `$aformat_ja$` | The format of the first **japanese** audio track
| `$achannels_en$` | The channel layout of the first **english** audio track

| By type & language with number |  |
| ----- | ------- |
| `$aformat_ja_1$` | The format of the **second japanese** audio track

If you want to see the regex in detail or test your results see [the regex101](https://regex101.com/r/NYzJyz/1).

-----

## Basic Usage

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