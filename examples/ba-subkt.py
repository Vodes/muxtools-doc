# ruff: noqa: F405 F403
from muxtools import *

episode = int(input("Please enter an episode number: "))

setup = Setup(
    f"{episode:02d}",
    None,
    show_name="Blue Archive",
    out_name=R"$show$ - S01E$ep$ (BD 1080p HEVC) [Kaleido-Test-Mux]",
    mkv_title_naming=R"$show$ - S01E$ep$ - $title$",
    out_dir="muxed",
    clean_work_dirs=False,
)

video_file = GlobSearch(f"*Kaleido*Archive* - S01E{setup.episode}*.mkv", dir="D:/")

# Use timecodes from video for calculations in shifts and merges and what not
# This is technically optional but you will get spammed with warnings.
setup.set_default_sub_timesource(video_file)

premux = Premux(video_file, subtitles=None, keep_attachments=False, mkvmerge_args=["--no-global-tags", "--no-chapters"])

sub_kaleido = SubFile(GlobSearch("*.ass", allow_multiple=True, dir=f"./{setup.episode}"))

chapters = Chapters.from_sub(sub_kaleido, use_actor_field=True) # Doing this later would grab stuff from the NCs lol

if episode not in [1, 12]:
    # Non-default shift_mode because that's what subkt uses.
    # I don't think shifting by time directly should be considered good practice but people want to match the behavior I guess.
    sub_kaleido.merge("./NCOP1/BlueArchive NCOP1.ass", "opsync", "sync", no_error=True, shift_mode=ShiftMode.TIME)
    sub_kaleido.merge("./NCED1/BlueArchive NCED1.ass", "edsync", "sync", no_error=True, shift_mode=ShiftMode.TIME)

sub_kaleido.merge("./common/warning.ass")
sub_kaleido.clean_garbage().clean_extradata().set_headers(
    (ASSHeader.PlayResX, 1920),
    (ASSHeader.PlayResY, 1080),
    (ASSHeader.LayoutResX, 1920),
    (ASSHeader.LayoutResY, 1080),
    (ASSHeader.YCbCr_Matrix, "TV.709"),
    (ASSHeader.ScaledBorderAndShadow, True),
    (ASSHeader.WrapStyle, 2),
    ("Title", "Kaleido-subs")
)

sub_enm = sub_kaleido.copy().autoswapper()

sub_official = SubTrack(f"./{setup.episode}/BlueArchive {setup.episode} - Dialogue (Nexon).srt", "English (Official/Nexon)", "en", False)
# Alternatively convert to ass with
# SubFile.from_srt(f"./{setup.episode}/BlueArchive {setup.episode} - Dialogue (Nexon).srt")

fonts = sub_kaleido.collect_fonts(use_system_fonts=False)

mux(
    premux,
    sub_kaleido.to_track("English", "en"),
    sub_enm.to_track("English (Honorifics)", "enm"),
    sub_official,
    *fonts,
    chapters,
    tmdb=TmdbConfig(218833)
)
