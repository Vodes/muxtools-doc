# External Dependencies

Practically everything is optional and you only need what you want to use.<br>
**FFMpeg** and **MKVToolnix** are used for just about anything you could do with muxtools though so keep that in mind.

## TLDR, I don't care
Most of the stuff you actually need can now be handled through [binary management](binary-management.md).<br>
You can just add the tools you want to your project and let muxtools take care of the rest.

Not everything here is in the catalog though, so this list is still useful if you need something more specific.

Everything that *is* covered however, can also be freely downloaded via the [muxtools-binaries](https://github.com/Vodes/muxtools-binaries/releases) repo.<br>
Which may or may not have more up-to-date and/or more optimized binaries for various stuff.

## Video encoders

- [x265](http://msystem.waw.pl/x265)
- [x264](https://download.videolan.org/x264/binaries)
- [SVT-AV1-Essential](https://github.com/nekotrix/SVT-AV1-Essential)
- [SVT-AV1-5fish](https://github.com/5fish/SVT-AV1)

FFV1 & ProRes are included with FFMPEG (see below)

## Other Utilities

- [FFMPEG](https://ffmpeg.org/download.html?aemtn=tg-on#build-windows)<br>
  Probably the most important utility for this package.<br>
  It's used for TTA, FLAC, W64 and AIFF audio encoding and also ensures valid input for every other encoder.<br>
  Also used to extract existing audio track from other releases/containers.<br>
  Oh and of course used for FFV1 lossless video encoding.<br><br>
  If you're interested in AAC encoding via [FDK AAC](https://trac.ffmpeg.org/wiki/Encode/AAC#fdk_aac) you might be interested in non-free builds like [my own](https://github.com/Vodes/FFmpeg-Builds) on GitHub or [on scoop](https://scoop.sh/#/apps?q=ffmpeg+ytdlp+nonfree).
- [eac3to](https://www.videohelp.com/software/eac3to)
- [SoX](https://sox.sourceforge.net/)
- [MKVToolNix](https://mkvtoolnix.download/downloads.html)/mkvmerge/mkvextract
- [opus-tools](https://www.opus-codec.org/downloads/)<br>
  Used for opus encoding.<br>
  The official builds are yet to receive any updates for whatever reason so for the time being I'd recommend getting builds from [rarewares](https://www.rarewares.org/opus.php).
- [qaac](https://github.com/nu774/qaac/releases)<br>
  The best encoder for AAC, but it does ALAC aswell.<br>
  This one has a few quirks, like needing iTunes either installed or its libraries.<br>
  [Here's](https://github.com/nu774/qaac/wiki/Installation) some detailed information in that and here are links to both [iTunes Libs](https://github.com/AnimMouse/QTFiles/releases) and a [libFLAC](https://github.com/xiph/flac/releases) you might need.<br>
- [FLAC (libFLAC)](https://github.com/xiph/flac/releases)<br>
  Used for FLAC encoding
- [CUETools](http://cue.tools/wiki/CUETools_Download)<br>
  Also used for FLAC encoding but with the FLACCL encoder instead.
- [LossyWAV](https://hydrogenaud.io/index.php/topic,112649.0.html)<br>
  A lossy preprocessor you can use for FLAC and Wavpack to achieve smaller sizes.<br>
  Doesn't really have any advantage over a good lossy codec besides being funny.
- [Wavpack](https://www.wavpack.com)<br>
  Another lossless Codec one can use if they feel like it.<br>

- [Aegisub](https://github.com/arch1t3cht/Aegisub) and [aegisub-cli](https://github.com/Myaamori/aegisub-cli)<br>
  Aegisub is basically *the* go-to subtitle editor. Useful for all kinds of subtitle related stuff.<br>
  Aegisub-CLI is (currently) only used for resampling in muxtools. Simply download it and place it right into your aegisub install folder.<br>
  (And don't forget to make sure that the install folder is also in your PATH)<br><br>
  For better resampling results, you might wanna get the `Resample Perspective` script in the Aegisub DependencyControl menu.
