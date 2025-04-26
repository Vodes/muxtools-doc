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