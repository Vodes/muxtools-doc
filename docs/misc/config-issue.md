Last updated: 2024-03-29

## Vodes-Nuke-VS-Guide™️ (the ultimate config issue solver)


- do you have python? if yes, nuke it and any site-packages (in appdata too)  folders
- uninstall vs and nuke plugins folder if you had it (%appdata%/Vapoursynth/plugins64) 
- Install Python ***3.12*** <br>(select for all users, when you click advanced or something like that in the installer)
- Install vapoursynth (select for all users)
- `pip install git+https://github.com/vapoursynth/vsrepo.git` (if it doesn't work out of the box) 
- install whatever plugins you need with vsrepo (run `vsrepo available` to see)
- `pip install vsjet vodesfunc vsmuxtools`