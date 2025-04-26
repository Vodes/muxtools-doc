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