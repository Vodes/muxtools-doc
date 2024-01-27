# Audio Encoding
## Available Encoders

There are plenty with varying degrees of usefulness.

### Lossless
- [FLAC (libFLAC)](https://github.com/xiph/flac/releases)
- [FLACCL](http://cue.tools/wiki/FLACCL) (included in CUETools)
- [FF_FLAC](https://ffmpeg.org/ffmpeg-codecs.html#flac-2) (FF = FFMPEG)
- [TTA/TrueAudio](http://tausoft.org/wiki/True_Audio_Codec_Overview)
- [Wavpack](https://www.wavpack.com/)
- ALAC via [qaac](https://github.com/nu774/qaac)

### Lossy
- Opus via [opusenc](https://opus-codec.org/downloads/)
- AAC via [qaac](https://github.com/nu774/qaac)
- AAC via FDK_AAC (in [non-free builds](https://scoop.sh/#/apps?q=ffmpeg-nonfree) of ffmpeg but also works with the [binary](https://github.com/nu774/fdkaac))
- [LossyWAV](https://hydrogenaud.io/index.php/topic,112649.0.html) (This one is a lossy preprocessor for other lossless codecs to save size)

## Available Extractors/Trimmers

### Extractors
- [FFMPEG](https://ffmpeg.org/)
- [eac3to](https://www.videohelp.com/software/eac3to)

Eac3to is at this point fully obsolete because of our ffmpeg implementation.<br>
There's only really a use for it if you need to add silence to something proprietary like TrueHD Atmos or DTS:X without reencoding.

### Trimmers
- [FFMPEG](https://ffmpeg.org/)
- [SoX](https://sox.sourceforge.net/)

SoX only works with lossless files and always uses wav internally.<br>
It also is more accurate than FFMPEG and as such should be your default for lossless.<br>
FFMPEG can somewhat decently trim and concat lossy audio and we implemented something similar to the eac3to delay thing to have a more accurate end result.

## Basic Usage
### All-in-one Function
There's this neat little `do_audio` function that should satisfy all your needs.<br>
If you don't pass any extractors, trimmers or encoders it will choose:

- FFMPEG as the extractor

- SoX or FFMPEG for the trimmer depending on if the input is lossy (the latter if it is)

- Opus as the encoder if lossless and otherwise it will choose to not encode


If you already have wav files to work with you can also pass `None` to the extractor param to skip that step.

```py
from vsmuxtools import src_file, Wavpack, do_audio # Another alias for this would be encode_audio

file = R"00008.m2ts"
audio = do_audio(file, 1, encoder=Wavpack())

# You can also pass a src_file with the vs(!)-muxtools extension.
# This will automatically apply the src_file trim if you don't pass any yourself.
ITBD = src_file(file, trim=(24, -24))
audio = do_audio(ITBD, 0)

# If you want to choose everything
from vsmuxtools import FFMpeg, Sox, TrueAudio

audio = do_audio(JPBD, track=0, extractor=FFMpeg.Extractor(preserve_delay=False), trimmer=Sox(), encoder=TrueAudio())
```

### Step by step

Of course you're not forced to use `do_audio`.

```py
from vsmuxtools import FFMpeg, Sox, FLAC, DitherType, src_file, Resample

ITBD = src_file(R"00008.m2ts", trim=(24, -24))

audio = FFMpeg.Extractor(track=1).extract_audio(ITBD.file)
audio = Sox(trim=[(24, 500), (800, 1245)], fps=Fraction(24000, 1001)).trim_audio(audio)
audio = FLAC(preprocess=Resample(dither=DitherType.LOW_SHIBATA)).encode_audio(audio)
```

All of those `audio` variables are a `AudioFile` object.<br>
To get the filepath you simply do `audio.file`.<br><br>

Same deal as with the [encodes](/guide/encode-video) these also have a `to_track()` function to create a track with metadata. (Defaults to `lang='jp', default=True, forced=False`)

### Preprocessing

(Almost) every encoder also supports various preprocessing options.<br>
Currently implemented are:

- Resample<br>
  To change sample rate or bitdepth

- Downmix / Pan<br>
  The ffmpeg [pan](http://ffmpeg.org/ffmpeg-all.html#pan-1) filter with a few [presets](/muxtools/audio/preprocess/#muxtools.audio.preprocess.Downmix.ATSC) for better/more dynamic downmixing

- Loudnorm<br>
  A ffmpeg based normalization implementation according to EBU-R128 standards.<br>
  This also uses the two-pass methodology as described [here](https://web.archive.org/web/20230308152626/https://wiki.tnonline.net/w/Blog/Audio_normalization_with_FFmpeg) and used in the ffmpeg-normalize utility.

#### Example usage
```py
# Lossless encoders use the Resample preprocessor by default (which defaults to 16bit and 48kHz)
audio = do_audio(file, 1, encoder=FLAC())

# Can be entirely disabled like this
audio = do_audio(file, 1, encoder=FLAC(preprocess=None))

# You can also chain them like this
audio = do_audio(file, 1, encoder=FLAC(preprocess=[Pan(Pan.RFC_7845), Resample(DitherType.LIPSHITZ)]))

# Or define your own with either ffmpeg args or an ffmpeg audio-filter
audio = do_audio(file, 1, encoder=FLAC(preprocess=[
    Resample(DitherType.LIPSHITZ),
    # In this case, the filter creates a massive echo effect (the args are obviously nonsense)
    CustomPreprocessor(filt="aecho=0.8:0.9:1000:0.3", args=["--example", "value"])
]))
```