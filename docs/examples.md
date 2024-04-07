### Muxing of my Jigokuraku fansub

<details>
  <summary>config.ini</summary>

```ini
[SETUP]
bdmv_dir = ./
show_name = Jigokuraku
allow_binary_download = True
clean_work_dirs = True
out_dir = muxed
out_name = [Nirvana] $show$ - S01E$ep$ [WEB 1080p HEVC] [$crc32$]
mkv_title_naming = Hell's Paradise - $ep$ - $title$
```

</details>
<details>
  <summary>Script</summary>

```py
from muxtools import Setup, Premux, GlobSearch, SubFile, mux, TitleTMDB

setup = Setup("09")

premux = Premux(f"./premux/Jigokuraku - {setup.episode} (premux).mkv")

dialogue = GlobSearch("*Dialogue*.ass", dir=f"./{setup.episode}/")
typesetting = GlobSearch("*TS*.ass", dir=f"./{setup.episode}/").paths
if not typesetting:
    typesetting = GlobSearch("*Sign*.ass", dir=f"./{setup.episode}/").paths

songs = ["./songs/OP.ass", "./songs/ED.ass"]
sub = SubFile([dialogue.paths, typesetting]) \
    .merge(songs[0], "opsync").merge(songs[1], "edsync")

fonts = sub.collect_fonts()

mux(premux, sub.to_track("English"), *fonts, tmdb=TitleTMDB(117465))
```
</details>

### Batch Mux script for a private cyberpunk mux
<details>
  <summary>Script</summary>

```py
from muxtools import Setup, GlobSearch, Premux, SubFile, mux, TmdbConfig

for i in range(1, 11):
    # Basic Setup for every episode without a config file
    setup = Setup(
        f"{i:02d}",  # Format to have padded zeros
        None,
        show_name="Cyberpunk Edgerunners",
        out_dir=R"D:\Compings\muxed",
        mkv_title_naming=R"$show$ - S01E$ep$ - $title$",
        out_name=R"[Styx] $show$ - S01E$ep$ [WEB 1080p HEVC]",
        clean_work_dirs=True,
    )
    bobbington = GlobSearch(f"*choom* - {setup.episode}*.mkv", dir=R"D:\Compings\b")
    nfweb = GlobSearch(f"*Cyberpunk Edgerunners - {setup.episode}*GerEngSub*.mkv", dir=R"D:\Compings\b")

    premux = Premux(
        bobbington,
        keep_attachments=False,
        subtitles=None,
        mkvmerge_args='--no-global-tags --track-name 0:"choom/MTBB Encode" --track-name 1:"Japanese 5.1 (Netflix)"',
    )

    audios = Premux(
        nfweb,
        video=None,
        audio=[0, 1],
        subtitles=None,
        keep_attachments=False,
        mkvmerge_args='--no-global-tags --no-chapters --track-name 1:"German 5.1 (Netflix)" --track-name 2:"English 5.1 (Netflix)"',
    )
    sub_en = SubFile.from_mkv(bobbington.paths, 0).clean_styles()
    sub_ger = SubFile.from_mkv(nfweb.paths, 1).clean_styles()
    sub_ger_signs = SubFile.from_mkv(nfweb.paths, 0).clean_styles()

    # Every font collector call will just dump them into the workdir and then return all including ones are already there.
    sub_ger_signs.collect_fonts()
    sub_en.collect_fonts()
    fonts = sub_ger.collect_fonts()

    mux(
        premux,
        audios,
        sub_en.to_track("English (whomst modified)"),
        sub_ger.to_track("German (Netflix modified)", "ger", False, False),
        sub_ger_signs.to_track("German Signs & Songs (Netflix)", "ger", False, True),
        *fonts,
        tmdb=TmdbConfig(105248, write_title=True, write_ids=True),
    )
```
</details>

### Basic encode script with multiple sources

<details>
    <summary>Script</summary>
    
```py
from vsmuxtools import * # Doing this is technically bad practise but I don't really have to worry about name collision here
from vspreview import is_preview
from awsmfunc import fixlvls
from vodesfunc import out

import JJKcommon as common
import JJKbdmvs as bdmv

setup = Setup("03")

stronger_deband = []
lol_deband = []
heavy_aa = []
wtf = []
lower_thresh = []

op_start_frame = 4603
ed_start_frame = 30569

zone_up = []
zone_slightly = []
zone_down = [(16064, 16303)]

if op_start_frame != -1:
    lol_deband.append((op_start_frame + 1167, op_start_frame + 1177))
    lol_deband.append((op_start_frame + 1383, op_start_frame + 1399))
    zone_slightly.append((op_start_frame, op_start_frame + 2157))

ITBD = FileInfo(bdmv.get_episode_itbd(), force_lsmas=True, trim=(12, -12))
DEBD = FileInfo(bdmv.get_episode_debd(), force_lsmas=True)
UKBD = FileInfo(bdmv.get_episode_ukbd(), force_lsmas=True)
KAIZOKU = FileInfo(
    GlobSearch(f"*Jujutsu Kaisen - {setup.episode}*.mkv", dir=R"\\diablo\Vault\Misc\Media\[Kaizoku] Jujutsu Kaisen (BD 1080p)"),
    force_lsmas=True,
)

filtered = common.filter_chain(ITBD.init_cut(), stronger_deband, heavy_aa, wtf, lol_deband)

chapters = Chapters(ITBD, _print=False).set_names(["Prologue", "Opening", "Part A", "Part B", "Ending", "Preview"]).print()

if is_preview():
    out(ITBD.src_cut, "ITBD")
    out(filtered[0], "Filtered")
    out(fixlvls(DEBD.init_cut()), "DEBD (Gamma fixed)")
    out(UKBD.src_cut, "UKBD")
    out(KAIZOKU.src_cut[:2] + KAIZOKU.src_cut, "Kaizoku")
    print(lol_deband)
else:
    settings = sb265(7, 13.7, rect=False, tskip=True, append="--aq-bias-strength 0.9")
    zones = [(a, b, 1.2) for a, b in zone_up]
    zones.extend([(a, b, 1.1) for a, b in zone_slightly])
    zones.extend([(a, b, 0.8) for a, b in zone_down])

    jp, en, de = encode_audio(ITBD, 1), encode_audio(UKBD), encode_audio(DEBD)
    video = x265(settings, zones, qp_clip=ITBD).encode(filtered[0])
    mux(
        video.to_track("Vodes Encode"),
        jp.to_track("Japanese 2.0"),
        en.to_track("English 2.0", "en"),
        de.to_track("German 2.0", "de"),
        chapters,
        tmdb=TmdbConfig(95479),
    )
```

</details>