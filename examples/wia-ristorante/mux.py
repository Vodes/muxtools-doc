from muxtools import Setup, VideoTrack, AudioTrack, SubTrack, TitleTMDB, mux
from fractions import Fraction


audio_delays = (9, -8, 9, 15, 9, -8, 9, -8, 9, 0, 6)

for i in range(1, 11 + 1):
    setup = Setup(
        f"{i:02d}",
        show_name="Ristorante Paradiso",
        allow_binary_download=False,
        clean_work_dirs=True,
    )

    video = VideoTrack(rf"{setup.bdmv_dir}\Video\{setup.episode}.avc", name="Netflix WEB-DL")
    audio = AudioTrack(
        rf"{setup.bdmv_dir}\Audio\{setup.episode}.ac3", name="Japanese 2.0 AC-3", delay=audio_delays[i - 1]
    )
    subtitles = SubTrack(rf"{setup.bdmv_dir}\Subtitles\{setup.episode}.sup", name="Full Subtitles (Right Stuf)")

    mux(video, audio, subtitles, rf"{setup.bdmv_dir}\Chapters\{setup.episode}.xml", tmdb=TitleTMDB(34855))  # type: ignore


ncs = ("NCOP", "NCED")
names = ("Marigold", "Suteki na Kajitsu")
sar = Fraction(6, 5) * 720 / 480

for i in range(len(ncs)):
    setup = Setup(
        ncs[i],
        show_name="Ristorante Paradiso",
        allow_binary_download=False,
        clean_work_dirs=True,
    )

    setup.edit("title", names[i])
    setup.edit("out_name", "[Aergia] $show$ - $ep$ (DVDRemux 480p MPEG-2 AC-3)")

    video = VideoTrack(
        rf"{setup.bdmv_dir}\Video\{setup.episode}.mpg",
        name="R2J DVD",
        crop=(0, 0, 0, 2),
        args=["--display-dimensions", f"0:{sar.numerator}x{sar.denominator}"],
    )
    audio = AudioTrack(rf"{setup.bdmv_dir}\Audio\{setup.episode}.ac3", name="Japanese 2.0 AC-3")
    subtitles = SubTrack(rf"{setup.bdmv_dir}\Subtitles\{setup.episode}.sup", name="Full Subtitles (Right Stuf)")

    mux(video, audio, subtitles)  # type: ignore