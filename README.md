## WARNING - WIP, new versions of BSIPA and the death of Modsaber have killed this - still working on fixing it. 
## To anyone trying to get this to work, note my 'winhttp.reg' file just added - this is necessary for _any_ mods to work now
# bsmodinstaller.py
Downloads and installs Beat Saber SongLoader, SyncSaber &amp; Other Mods. Always the latest version, so you can re-run the script to freshen your mods to their latest release!

# Linux Instructions
Requires wine & winetricks installed.
Copy bsmodinstaller.py to your 'Beat Saber' directory and run it.
Install dotnet472 (other versions may also work) with command provided at the printout at the end of the script.

# Windows instructions
1. Install Python 3 if you don't already have it.
2. Open up a CMD or PS window in the Beat Saber directory (Shift + Right Click -> Open In PS/Command).
3. Run 'python -m pip install requests' to install requests dependency.
4. Run installer with 'python .\bsmodinstaller.py' or double click the file.

# Optionally
Review script and disable mods that you don't want installed by setting "enabled" to False in the dictionary.

# TODO:
- Test and confirm that it can be run at every game launch to update the DLLs through Steam Launch Options without any major delays.
- Add more mods and an easy menu for selecting which mods to install.
