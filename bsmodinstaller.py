#!/usr/bin/env python3
"""
Downloads and installs the latest version of various Beat Saber mods.
"""
import os
import subprocess
import sys
from io import BytesIO
from zipfile import ZipFile
import requests

MODS = [
    {
        "name": "songloader",
        "url": "https://www.modsaber.org/registry/song-loader/",
        "enabled": True,
        "type": "modsaber",
    },
    {
        "name": "songbrowser",
        "url": "https://www.modsaber.org/registry/songbrowserplugin",
        "enabled": True,
        "type": "modsaber",
    },
    {
        "name": "beatsaverdownloader",
        "url": "https://www.modsaber.org/registry/beatsaverdownloader",
        "enabled": True,
        "type": "modsaber",
    },
    {
        "name": "customui",
        "url": "https://www.modsaber.org/registry/customui/",
        "enabled": True,
        "type": "modsaber",
    },
    {
        "name": "scoresaber",
        "url": "https://www.modsaber.org/registry/scoresaber",
        "enabled": True,
        "type": "modsaber",
    },
    {
        "name": "YUR Fit",
        "url": "https://www.modsaber.org/registry/yurfit/",
        "enabled": True,
        "type": "modsaber",
    },
    {
        "name": "nsjson",
        "url": "https://www.modsaber.org/registry/newtonsoft-json",
        "enabled": True,
        "type": "modsaber",
    },
    {
        "name": "harmony",
        "url": "https://www.modsaber.org/registry/harmony",
        "enabled": True,
        "type": "modsaber",
    },
    {
        "name": "syncsaber",
        "url": "https://www.modsaber.org/registry/syncsaber",
        "enabled": True,
        "type": "modsaber",
    }
]

class ModInstaller:
    '''Installer for Beat Saber mods'''
    @staticmethod
    def install_mod(mod: dict):
        '''Installs a given mod'''
        if mod['enabled'] is True:
            if mod['type'] == 'modsaber':
                modsaber_url = mod.get('url')
                mod_name = mod.get('name')
                print('Installing %s from modsaber...' %(mod_name))
                modsaber_meta_data = requests.get(modsaber_url).json()
                zip_url = modsaber_meta_data.get('files', {}).get('steam', {}).get('url')
                zip_data = BytesIO(requests.get(zip_url).content)
                ZipFile(zip_data).extractall()
            elif mod['type'] == 'brian91292_dll':
                metadata_url = mod.get('url')
                dll_dest = mod.get('destination')
                mod_name = mod.get('name')
                print('Installing %s to %s...' %(mod_name, dll_dest))
                metadata = requests.get(metadata_url).json()
                dll_url = metadata.get('assets', [])[0].get("browser_download_url")
                dll_contents = requests.get(dll_url).content
                with open(dll_dest, 'wb') as library:
                    library.write(dll_contents)

    @staticmethod
    def inject_ipa():
        '''Runs the IPA Unity injector against Beat Saber.exe'''
        if os.name != 'nt':
            os.environ['WINEPREFIX'] = os.path.realpath('../../compatdata/620980/pfx/')
            subprocess.run('wine ./IPA.exe "Beat Saber.exe"', shell=True)
        else:
            subprocess.run('IPA.exe "Beat Saber.exe"', shell=True)

if __name__ == '__main__':
    if os.getcwd().split(os.sep)[-1] != "Beat Saber":
        sys.exit("Please run this from the Beat Saber directory")

    if not os.path.isdir('./UserData'):
        os.mkdir('./UserData')

    for item in MODS:
        ModInstaller.install_mod(item)

    if os.path.isdir('./IPA/Backups') and len(os.listdir('IPA/Backups/Beat Saber')) != 0:
        print("IPA.exe has already been run. Skipping.")
    else:
        ModInstaller.inject_ipa()

    print("Mods installed successfully!")
