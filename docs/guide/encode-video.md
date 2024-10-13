# Video Encoding

## x264 & x265
Lossy encoders targetting quality.
These two also support resuming from previous parts of the encode in case it crashed or whatever. <br>
It's done somewhat automagically and you don't really have to worry about it.

## FFV1
FFMPEG's lossless codec.<br>
Basically *the* lossless codec to use. Supports just about everything and has way better compression than lossless x264.

## LosslessX264
Another option for lossless encodes.<br>
Way worse compression than FFV1 but also way faster. Limited to 10 bit video.

## SVTAV1
An AV1 encoder that has proper threading capabilities standalone and is still competitive with others.
You can of course use [SVT-AV1-PSY](https://github.com/gianni-rosato/svt-av1-psy) with muxtools too.

---------
## Basic Usage
```py
from vsmuxtools import src_file, x265, x264, FFV1, LosslessX264, LosslessPreset, settings_builder_x265, settings_builder_x264
from vstools import vs, core, finalize_clip

JPBD = src_file(R"F:\BDMV\Main Disc\BDMV\STREAM\00002.m2ts", True, (24, 500))

# This calls initialize_clip from vstools which creates a 16 bit clip to work with
src = JPBD.init_cut()

filtered = denoise(src)
filtered = grain(filtered)

output = finalize_clip(filtered)

# This will run if the current script is started without vspreview and whatnot
# Alternatively you can use: if not vspreview.is_preview():
if __name__ == "__main__":
    # Convenience function to make a settings string
    settings = settings_builder_x265(preset="slower", crf=13.5)

    # Basic bitrate multiplier zones
    x265_zones = [(100, 400, 0.5), (450, 480, 1.25)]

    # QP Clip can be a normal videonode or the src_file/FileInfo
    # You can also pass existing files to the qp_file parameter
    video_hevc = x265(settings, x265_zones, qp_clip=JPBD).encode(output)

    # x264 Zones can be a bit more useful with params like crf
    # You can still pass stuff like this with x265 but it can only do b and q.
    x264_zones = [(100, 400, "crf", 15), (450, 480, "crf", 13)]

    # You can also use a file with settings tho there's also a settings builder for x264
    # QP file generation will be skipped in this example
    video_avc = x264(R"./path/x264_settings", x264_zones).encode(output)

    # These two have way less params and don't support resumable encodes.
    # You only really have to care about the 3 presets this package offers.
    video_ffv1 = FFV1(LosslessPreset.COMPRESSION).encode(output)
    video_ll_avc = LosslessX264(LosslessPreset.SPEED).encode(output)
```

All of those `video_*` variables return a `VideoFile` object.<br>
To get the filepath you simply do `video_hevc.file`.<br><br>
Here you can also have your first look at the `to_track()` function of the `*File` types.<br>
These convert the File types to their respective track types. This will be needed for muxing later.

-------

## Intermediaries

vs-muxtools **0.2.0+** has convenience classes for creating an intermediary and encoding that to one or many targets.

```py
# Encode clip to FFV1 first and then to the list of encoders (x265 and SVTAV1)
IntermediaryEncoder(
    LosslessX264(LosslessPreset.SPEED),
    [
        x265(settings_builder_x265("veryslow", 13.5)),
        SVTAV1(4, 18),
    ],
).encode(clip)

# Can also do something like this

IntermediaryEncoder(
    LosslessX264(LosslessPreset.SPEED),
    [
        x265(settings_builder_x265("veryslow", 13.5)),
        (SVTAV1(4, 18), lambda clip: Hermite.scale(clip, 1280, 720)), # Downscales the intermediary and outputs that to SVTAV1
    ],
).encode(clip)
```

There's also a standalone [ProResIntermediary](/vs-muxtools/video/encoders/intermediary/#vsmuxtools.video.encoders.intermediary.ProResIntermediary) class that automatically handles conversion to and from 422.<br>
The approach may still be very flawed but it didn't cause issues at a quick glance.