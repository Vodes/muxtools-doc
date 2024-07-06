# Wav and Friends

So you've probably heard of wav and w64 before.<br>
This page is meant to explain most notable containers to contain pcm with.

## Formats

### W64

##### [Specification](https://web.archive.org/web/20230528132944/https://www.ambisonia.com/Members/mleese/sony_wave64.pdf/sony_wave64.pdf)

Also known as Sony Wave64.<br>
This is an extension to the original riff specification to add support for bigger files.

??? info "Usage FFMPEG"
    
    ```bash
    ffmpeg -i "$input" -c:a pcm_s24le out.w64
    ```

### RF64

##### [Specification](https://web.archive.org/web/20230507102826/https://tech.ebu.ch/docs/tech/tech3306v1_0.pdf) | [Wikipedia](https://en.wikipedia.org/wiki/RF64)

This is an extension to the original riff specification by the European Broadcasting Union.<br>
It has been accepted as the ITU recommendation [ITU-R BS.2088](https://www.itu.int/rec/R-REC-BS.2088-1-201910-I/en).

??? info "Usage FFMPEG"
    
    ```bash
    # Auto means that it'll be regular wav until it exceeds 4GB.
    ffmpeg -i "$input" -c:a pcm_s24le -rf64 auto out.wav
    ```

### AIFF

Audio Interchange File Format

##### [Specification](https://web.archive.org/web/20171118222232/http://www-mmsp.ece.mcgill.ca/documents/audioformats/aiff/aiff.html) | [Wikipedia](https://en.wikipedia.org/wiki/Audio_Interchange_File_Format)

Essentially the Apple equivalent of the regular RIFF/WAVE format and also limited to 4GB.<br>
Not recommended.

??? info "Usage FFMPEG"
    
    ```bash
    ffmpeg -i "$input" -c:a pcm_s24be out.aiff
    ```

### CAF
Core Audio Format

##### [Specification](https://web.archive.org/web/20240415092937/https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_overview/CAF_overview.html#//apple_ref/doc/uid/TP40001862-CH209-TPXREF101) | [Wikipedia](https://en.wikipedia.org/wiki/Core_Audio_Format)

Essentially the Apple equivalent of RF64.

??? info "Usage FFMPEG"
    
    ```bash
    ffmpeg -i "$input" -c:a pcm_s24le out.caf
    ```

## What should I use

If you're mainly using Apple devices and software exclusive to that ecosystem the answer is simple: CAF.

If not: The answer is complicated.<br>
From my own experience and from what I gathered in various forum posts[^1][^2] and blogs[^3][^4]<br>
**RF64 is more widely supported by both hardware and software.**

### The chaotic good

If your software supports it... you should just **use FLAC**.<br>
There's no gamble if it supports one or any of the 64-bit WAV extensions/deviations. It usually either supports FLAC or it doesn't.

With FLAC you get a more concrete spec that software is less likely to misinterpret and other things[^5] less useful for the purpose of having an intermediary file.

??? info "Usage"
    
    ```bash
    # If you don't care about compression and just want speed
    flac -0 -o "out.flac" "$input"

    # The reference flac encoder is better but ffmpeg is also an option
    ffmpeg -i "$input" -c:a flac -compression_level 0 "out.flac"
    ```

[^1]: [https://gearspace.com/board/music-computers/1086321-do-you-use-rf64.html](https://gearspace.com/board/music-computers/1086321-do-you-use-rf64.html)
[^2]: [https://forums.cockos.com/showpost.php?s=10bbd1b868d37f653ec4e36a6de1cb5a&p=1845069&postcount=2](https://forums.cockos.com/showpost.php?s=10bbd1b868d37f653ec4e36a6de1cb5a&p=1845069&postcount=2)
[^3]: [Bjorn Roche - WAVE64 vs RF64 vs CAF](https://web.archive.org/web/20231210135558/http://blog.bjornroche.com/2009/11/wave64-vs-rf64-vs-caf.html)
[^4]: [https://trptk.com/one-wav-or-the-other-wav-formats-explained](https://trptk.com/one-wav-or-the-other-wav-formats-explained)
[^5]: Integrity checks in the encoder and error detection in the decoder, actual metadata support, obviously lossless compression