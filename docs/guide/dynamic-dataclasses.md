# Dynamic Dataclasses

Since (vs-)muxtools **0.2.0** all video and audio encoders use [pydantic dataclasses](https://docs.pydantic.dev/latest/concepts/dataclasses/).<br>
These allow users to pass kwargs to them.

These kwargs are used to pass custom params to the encoder processes.<br>
Have a look at part of the `CLIKwargs` class docstring here:
```py
test = Encoder(clip, colorspace="BT709")
print(test.get_custom_args())
# returns ['--colorspace', 'BT709']

# if it starts with an _ it will be a single - argument
# empty values will be stripped
test = Encoder(clip, _vbr="")
print(test.get_custom_args())
# returns ['-vbr']

# if it ends with an _ it will preserve underscores
test = Encoder(clip, _color_range_="limited")
print(test.get_custom_args())
# returns ['-color_range', 'limited']
```

#### Yes, `append` is still supported

... and now also *almost* everywhere and better!

```py
test = Encoder(clip, append="-vbr --bitrate 192")
test = Encoder(clip, append=["-vbr", "--bitrate", "192"])
test = Encoder(clip, append={"-vbr": "", "--bitrate": "192"})
# all of them return ['-vbr', '--bitrate', '192']
```


## Practical Uses

In terms of video encoders I mostly implemented this to serve SVTAV1 and the FFMPEG encoders.

You can for example do something like
```py
SVTAV1(qp_clip=src, sharpness=3, film_grain=3, tune=3, variance_boost_strength=3, variance_octile=5, frame_luma_bias=20)
```
and you will find that most of these params are not actually defined in the `SVTAV1` class constructor.<br>
They will however still get passed to it as `--sharpness 3 --film-grain 3 --variance-boost-strength 3 --variance-octile 5 --frame-luma-bias 20`.

This will also work for x264/5 but considering the settings there are just a string to begin with, I don't see much of a point.

## Affinity

This ***only***[^1] applies to the video encoders but you can now pass an `affinity` kwarg to the classes.

Just like the vs-tools [`set_affinity`](https://jaded-encoding-thaumaturgy.github.io/JET-guide/master/basics/babys-first-script/#affinity-and-memory-allocation) function, this will lock the process (of the encoder, instead of vapoursynth) to the cores you request.

A *fun* and interesting tidbit that inspired me to write this is that SVTAV1 seems to always inherit the affinity of the parent that started it.<br>
Which means that it would be locked to the same affinity you set for your filtering when using it through muxtools.<br>
muxtools [simply overwrites](https://github.com/Jaded-Encoding-Thaumaturgy/vs-muxtools/blob/a077af7ee2efaacd147f0227f8e150ea653f0a04/vsmuxtools/video/encoders/standalone.py#L198-L199) it to use all cores now if nothing custom was passed.

[^1]: Make an issue if you want to see that for audio stuff. Can't think of a usecase tho.