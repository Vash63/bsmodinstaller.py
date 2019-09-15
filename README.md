## WARNING - WIP, new versions of BSIPA and the death of Modsaber have killed this - still working on fixing it. 
## To anyone trying to get this to work, note my 'winhttp.reg' file just added - this is necessary for _any_ mods to work now
# bsmodinstaller.py
Downloads and installs Beat Saber SongLoader, SyncSaber &amp; Other Mods. Always the latest version, so you can re-run the script to freshen your mods to their latest release!
This script also installs .NET Framework 4.7.2 into the Beat Saber wine prefix. It is a requirement for the new BSIPA mod loader.
NOTE: This has been tested with Proton 4.2-3.

# Linux Instructions
Requires wine, winetricks and protontricks installed.
Requires the requests and packaging python modules.
Copy bsmodinstaller.py to your 'Beat Saber' directory and run it.

# Windows instructions
1. Install Python 3 if you don't already have it.
2. Open up a CMD or PS window in the Beat Saber directory (Shift + Right Click -> Open In PS/Command).
3. Run 'python -m pip install requests' to install requests dependency.
4. Run installer with 'python .\bsmodinstaller.py' or double click the file.

# Optionally
Review script and remove or add mods want installed to the BEATMODS list.
Some mods like SongBrowser are not part of beatmods. You can add such mods by using the RAWMODS list. The url value there can be either a local path or a web address.

# TODO:
- Test and confirm that it can be run at every game launch to update the DLLs through Steam Launch Options without any major delays.
- Add more mods and an easy menu for selecting which mods to install.
