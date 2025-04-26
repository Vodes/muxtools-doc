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