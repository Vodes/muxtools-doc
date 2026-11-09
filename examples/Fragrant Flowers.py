from muxtools import (
    Setup,
    GlobSearch,
    Premux,
    SubFile,
    mux,
    TmdbConfig,
    Chapters,
    VideoTrack,
    TimeScale,
)

ep = input("Enter episode number or range: ").split()

if len(ep) == 1:
    start = end = int(ep[0])
else:
    start, end = map(int, ep)

for i in range(start, end + 1):
    setup = Setup(
        f"{i:02d}",  # Format to have padded zeros
        None,
        show_name="The Fragrant Flower Blooms with Dignity",
        work_dir=R"F:\Sub Projects\The-Fragrant-Flower-Blooms-with-Dignity\Temp",
        out_dir=R"F:\Sub Projects\The-Fragrant-Flower-Blooms-with-Dignity",
        mkv_title_naming=R"$show$ - S01E$ep$ - $title$",
        out_name=R"[FLE] The Fragrant Flower Blooms with Dignity - S01E$ep$ (WEB 1080p HEVC AAC) [$crc32$]",
        clean_work_dirs=True,
    )

    setup.set_default_sub_timesource("24000/1001", timescale=TimeScale.MKV)

    video = GlobSearch(rf"E{setup.episode}*.265", dir=rf"F:\Sub Projects\The-Fragrant-Flower-Blooms-with-Dignity\E{setup.episode}")
    audio = GlobSearch(rf"*S01E{setup.episode}*.mkv", dir=r"F:\Sub Projects\The-Fragrant-Flower-Blooms-with-Dignity\Videos")
    dialogues = GlobSearch(r"*Dialogues.ass", dir=rf"F:\Sub Projects\The-Fragrant-Flower-Blooms-with-Dignity\E{setup.episode}")
    signs = GlobSearch(r"*Signs.ass", dir=rf"F:\Sub Projects\The-Fragrant-Flower-Blooms-with-Dignity\E{setup.episode}")
    songs = ["./Songs/OP.ass", "./Songs/ED.ass"]

    print(rf"Muxing Started for S01E{setup.episode}")

    encode = VideoTrack(video, "WEB / HEVC / 10 bits / 1080p / FLE", lang="und")

    jpn = Premux(
        audio,
        keep_attachments=False,
        mkvmerge_args='--no-track-tags --no-global-tags --no-video --no-subtitles --no-chapters --language 1:ja --track-name 1:"Japanese / AAC / 2.0 / Netflix"',
    )

    TS = (
        SubFile([signs.paths[0]])
        .merge(songs[0], "opsync", no_error=True, use_actor_field=True)
        .merge(songs[1], "edsync", no_error=True, use_actor_field=True)
        .clean_styles()
        .clean_comments()
        .clean_garbage()
        .clean_extradata()
    )
    FLE = SubFile(dialogues.paths[0]).merge(TS).clean_styles().clean_comments().clean_garbage().clean_extradata()
    fonts = FLE.collect_fonts()
    chap = Chapters.from_sub(signs)

    mux(
        encode,
        jpn,
        FLE.to_track(r"Full Subtitles / English / ASS / FLE"),
        chap,
        *fonts,
        tmdb=TmdbConfig(id=271607, season=1, write_title=True, write_ids=True),
        quiet=True,
    )
