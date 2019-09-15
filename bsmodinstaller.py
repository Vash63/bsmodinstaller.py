#!/usr/bin/env python3
"""
Downloads and installs the latest version of various Beat Saber mods. This has been tested with proton 4.2-3.
"""
import os
import subprocess
import sys
from io import BytesIO
from zipfile import ZipFile
import requests
from packaging import version

# simply list the mods you like on beatmods.com here by name
BEATMODS = [
"songloader",
"beatsaverdownloader",
"scoresaber",
"yur fit calorie tracker",
"syncsaber"
]

''' BEWARE: you have to get the dependencies for these mods yourself.
The url has to link directly to the .zip file containing a mod
we don't care if the url is a local path to a file or a web address, as in, starts with http

EXAMPLE:
RAWMODS = [
    {
        "name": "mod1",
        "url": "/local/path/to/your/mod1.zip"
    },
    {
        "name": "mod2",
        "url": "https://github.com/modauthor/mod2/releases/download/1.0.0/mod2_1_0_0.zip"
    }
]
'''
RAWMODS = [
    {
        "name": "songbrowser",
        "url": "https://github.com/halsafar/BeatSaberSongBrowser/releases/download/3.0.5/SongBrowser_3_0_5.zip"
    }
]


beatmods_baseurl = 'https://beatmods.com'

# contents of the winhttp.reg file
winhttp = '''Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\\Software\\Wine\\DllOverrides]
"winhttp"="native,builtin"
'''

def install_mod(mod: dict):
    print('Installing %s' %(mod["name"]))
    if mod["url"].startswith("http"):
        zip_data = BytesIO(requests.get(mod["url"]).content)
        ZipFile(zip_data).extractall()
    else:
        with open(mod["url"], 'rb') as fin:
            zip_data = BytesIO(fin.read())
            ZipFile(zip_data).extractall()

def run_ipa():
    if os.name != 'nt':
        subprocess.run('protontricks -c \'wine ./IPA.exe "Beat Saber.exe"\' 620980', shell=True)
    else:
        subprocess.run('IPA.exe "Beat Saber.exe"', shell=True)

# this function can walk the mod dependencies recursively and add everything you need to the mod_list
def try_add_mod(mod_name: str, mod_data: dict, mod_list: list):
    for mod in mod_data:
        if mod["name"].lower() == mod_name.lower() or mod["_id"].lower() == mod_name:
            mod_in_list = False
            # First check if our mod_list already includes this mod
            for index, entry in enumerate(mod_list):
                if entry["name"] == mod["name"].lower():
                    mod_in_list = True
                    # Check if the version is higher
                    # We prefer the newer version. It'll probably break less things.
                    if version.parse(entry["version"]) < version.parse(mod["version"]):
                        mod_list[index]["url"] = beatmods_baseurl + mod["downloads"][0]["url"]
                        mod_list[index]["version"] = mod["version"]
                    break

            # skip to next required mod
            if mod_in_list == True:
                break

            mod_info = {}
            mod_info["name"] = mod_name.lower()
            mod_info["version"] = mod["version"]
            mod_info["url"] = beatmods_baseurl + mod["downloads"][0]["url"]
            mod_list.append(mod_info)

            # now loop through the dependencies and recursively call this function again
            for dep in mod["dependencies"]:
                # first check if dep is a string, subdependencies seem to be _id most of the time
                # call try_add_mod directly in this case.
                if isinstance(dep, str):
                    try_add_mod(dep, mod_data, mod_list)

                # extract the dep name otherwise
                else:
                    try_add_mod(dep["name"].lower(), mod_data, mod_list)

# this function takes the mod_data from beatmods and the users' required mods and builds a list of all mods including their dependencies
def create_mod_list(mod_data: dict, required_mods: list):
    mod_list = []

    # build our mod list out of the required mods and their dependencies
    for required_mod in required_mods:
        try_add_mod(required_mod, mod_data, mod_list)
    return mod_list

if __name__ == '__main__':
    if os.getcwd().split(os.sep)[-1] != "Beat Saber":
        sys.exit("Please run this from the Beat Saber directory")

    if not os.path.isdir('./UserData'):
        os.mkdir('./UserData')

    # fetch the beatmods json formatted mod data
    mod_data = requests.get('https://beatmods.com/api/v1/mod?search=&status=approved&sort=&sortDirection=1').json()
    # create a list of mods to-be-installed depending on the specified mods and their dependencies
    mod_list = create_mod_list(mod_data, BEATMODS)

    # add raw mods to the list
    for mod in RAWMODS:
        mod_list.append(mod)

    for item in mod_list:
        install_mod(item)

    if os.path.isdir('./IPA/Backups') and os.path.isdir('./IPA/Backups/Beat Saber') and len(os.listdir('IPA/Backups/Beat Saber')) != 0:
        print("IPA.exe has already been run. Skipping.")
    else:
        run_ipa()

    # fixes required to run Beat Saber with mods in proton
    if os.name != 'nt':
        # install .net framework 4.7.2 if not yet done, this has to be done before we override winhttp to native
        if not os.path.exists('../../compatdata/620980/pfx/drive_c/windows/dotnet472.installed.workaround'):
            print(".net framework 4.7.2 is missing, installing")
            subprocess.run('protontricks 620980 dotnet472', shell=True)

        # check if .net framework 4.7.2 has been installed but winhttp not yet overridden
        if os.path.exists('../../compatdata/620980/pfx/drive_c/windows/dotnet472.installed.workaround'):
            print("Override winhttp to native")

            with open('winhttp.reg', 'w', encoding="ascii") as winhttp_file:
                winhttp_file.write(winhttp)

            # run this with protontricks as well, else wine complains about differing wineserver versions
            subprocess.run('protontricks -c "wine regedit.exe winhttp.reg" 620980', shell=True)

    print("Mods installed successfully!")
