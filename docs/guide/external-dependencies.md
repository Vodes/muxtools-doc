# External Dependencies

**\*** = Cannot be auto downloaded on runtime<br>
\*\* = Cannot be downloaded using scoop

## Encoders

You only really need x264 and x265, depending on what you wanna use.<br>
I recommend these specific versions. Easily buildable on any platform if you're not on windows.

- [x265-aMod](https://github.com/DJATOM/x265-aMod)** (by DJATOM)
- [x264-aMod](https://github.com/DJATOM/x264-aMod)** (by DJATOM)

FFV1 is included with FFMPEG (see below)

## Other Utilities

- [FFMPEG](https://ffmpeg.org/download.html?aemtn=tg-on#build-windows)<br>
  Probably the most important utility for this package.<br>
  It's used for TTA, FLAC, W64 and AIFF audio encoding and also ensures valid input for every other encoder.<br>
  Also used to extract existing audio track from other releases/containers.<br>
  Oh and of course used for FFV1 lossless video encoding.<br><br>
  If you're interested in AAC encoding via [FDK AAC](https://trac.ffmpeg.org/wiki/Encode/AAC#fdk_aac) you might be interested in non-free builds like [these](https://github.com/AnimMouse/ffmpeg-autobuild/releases) on GitHub or [those](https://scoop.sh/#/apps?q=ffmpeg-nonfree) on scoop.
- [eac3to](https://www.videohelp.com/software/eac3to)
- [SoX](https://sox.sourceforge.net/)*
- [MKVToolNix](https://mkvtoolnix.download/downloads.html)/mkvmerge/mkvextract*
- [opus-tools](https://www.opus-codec.org/downloads/)<br>
  Used for opus encoding
- [qaac](https://github.com/nu774/qaac/releases)<br>
  The best encoder for AAC, but it does ALAC aswell.<br>
  This one has a few quirks, like needing iTunes either installed or its libraries.<br>
  [Here's](https://github.com/nu774/qaac/wiki/Installation) some detailed information in that and here are links to both [iTunes Libs](https://github.com/AnimMouse/QTFiles/releases) and a [libFLAC](https://github.com/xiph/flac/releases) you might need.<br>
- [FLAC (libFLAC)](https://github.com/xiph/flac/releases)<br>
  Used for FLAC encoding
- [CUETools](http://cue.tools/wiki/CUETools_Download)**<br>
  Also used for FLAC encoding but with the FLACCL encoder instead.
- [LossyWAV](https://hydrogenaud.io/index.php/topic,112649.0.html)***<br>
  A lossy preprocessor you can use for FLAC and Wavpack to achieve smaller sizes.<br>
  Doesn't really have any advantage over a good lossy codec besides being funny.
- [Wavpack](https://www.wavpack.com)<br>
  Another lossless Codec one can use if they feel like it.<br>

- [Aegisub](https://github.com/arch1t3cht/Aegisub)*** and [aegisub-cli](https://github.com/Myaamori/aegisub-cli)***<br>
  Aegisub is basically *the* go-to subtitle editor. Useful for all kinds of subtitle related stuff.<br>
  Aegisub-CLI is (currently) only used for resampling in muxtools. Simply download it and place it right into your aegisub install folder.<br>
  (And don't forget to make sure that the install folder is also in your PATH)<br><br>
  For better resampling results, you might wanna get the `Resample Perspective` script in the Aegisub DependencyControl menu.


## TLDR, I don't care
You can also use the `muxtools` CLI functionality to automatically install everything **not** marked with `**` on windows.<br>It will only ask you for tools you don't already have in PATH.

Simply run `muxtools <deps/dependencies>` and you will find yourself getting prompts for everything.

If you already have tools like SoX, Eac3to and qAAC installed, you might still want to have updated libraries for them.

To get those you can run `muxtools <libs/libraries>`.<br>
(No need to do so if you did `deps` before this because that will run both)