# Video Encoding

For available and/or recommended encoders, see [External Dependencies](external-dependencies.md).<br>
All of them are available through the [binary management](binary-management.md).

The `SVTAV1` class will use whichever `SvtAv1EncApp` comes first in your *managed* binaries or falls back to the first one in your **PATH**.<br>
So if you want to use managed SVT-AV1-Essential, only add that to your binary config.

The `FFV1` and `ProRes` classes just use their respective encoder in FFMpeg.

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

## Dolby Vision & HDR10+

The `x265` and `SVTAV1` encoders can pass through Dolby Vision and HDR10+ metadata.<br>
Static HDR10 metadata is picked up automatically from the first frame of the clip, so you generally don't have to do anything for that.

For the dynamic metadata you first create a helper from the source and pass it to the encoder.
This will take care of extracting the metadata and matching it to the source trim.

```py
from vsmuxtools import DolbyVision, HDR10Plus, x265

# The source has to actually contain Dolby Vision metadata of course.
# Profile 7 has to be converted to 8.1 for x265.
dovi = DolbyVision.from_source(JPBD).convert_profile("8.1")
hdr10plus = HDR10Plus.from_source(JPBD)

video_hevc = x265(
    settings,
    dolby_vision=dovi,
    hdr10plus=hdr10plus,
).encode(output)
```

You'll need `dovi_tool` and/or `hdr10plus_tool` installed for this to work.<br>
Both available through the [binary management](binary-management.md).<br>
You can also use existing sidecars with `DolbyVision.from_file("RPU.bin", profile="8.1")` and `HDR10Plus.from_file("metadata.json")`.

`x265` can keep Profile 5, 8.1, 8.2 and 8.4 metadata as-is, but Profile 7 needs to be converted to 8.1 first.<br>
`SVTAV1` turns Dolby Vision into the AV1 Profile 10 equivalent automatically, e.g. 5 becomes 10.0, 7 becomes 10.6 and 8.1 becomes 10.1.

!!! warning
    Profile 5 (and AV1 Profile 10.0) uses IPT-PQ-C2, whereas HDR10-compatible Profile 7, 8.1 and 10.1 use BT.2020/PQ.<br>
    `convert_profile("8.1")` only changes the RPU. It does **not** convert the clip's colorspace, so converting Profile 5 to 8.1/10.1 means you have to do that manually. Profile 7 is already HDR10 compatible.
    <br><br>
    Do note that this **is not** a simple zimg resample operation either because you need a valid HDR10 base-video.<br>
    You likely need to `placebo.Tonemap` with `DOVI` as `src_csp` and `HDR10` as `dst_csp`, **without tone- or gamut-mapping** and set appropriate HDR10 props afterwards (BT2020, ST2084, BT2020_NCL).<br>
    **I'm not sure myself whether that is the correct way of doing things!**

!!! note
    vs-muxtools **does not** handle the enhancement-layer that may be present on Dolby Vision *Profile 7* media, otherwise known as **EL** or **FEL**, for you.<br>
    They are usually separate video streams and there are plugins to apply it to your video within vapoursynth, like [vs-nlq](https://github.com/quietvoid/vs-nlq) or [felbaker](https://github.com/bbeny123/felbaker).<br>
    This is also what I would recommend you do.
    

If you trim, duplicate or remove frames after creating the helpers, do the same to the metadata too or it'll no longer match your encode.
`trim`, `duplicate` and `remove` are available on both helpers.<br>
For example, if you crop letterbox bars, you probably also want to update the Dolby Vision active area:

```py
output = output.std.Crop(top=132, bottom=132)
dovi = dovi.crop_active_area()
```

SVTAV1 supports this too, given an encoder build that actually supports the metadata options.
Dolby Vision AV1 needs to be output as IVF and muxed to MKV afterwards so the Dolby Vision configuration record gets written:

```py
from vsmuxtools import SVTAV1, mux

video_av1 = SVTAV1(
    dolby_vision=dovi,
    hdr10plus=hdr10plus,
).encode(output)

mux(video_av1.to_track(), outfile="encoded.mkv")
```

`SVTAV1` will disable WebM output if you pass Dolby Vision metadata, even if you give it a `.webm` filename.<br>
The encoder binaries differ quite a lot here, so make sure your build understands the HDR options and check the finished file with `ffprobe` or the relevant metadata tool.

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

There's also a standalone [ProResIntermediary](/reference/vsmuxtools/video/encoders/intermediary/#vsmuxtools.video.encoders.intermediary.ProResIntermediary) class that automatically handles conversion to and from 422.<br>
The approach may still be very flawed but it didn't cause issues at a quick glance.
