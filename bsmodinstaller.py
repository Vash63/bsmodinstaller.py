#!/usr/bin/env python3
import json,requests,os,subprocess
from io import BytesIO
from zipfile import ZipFile
from sys import exit

mods = [
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
        "name": "befitness",
        "url": "https://www.modsaber.org/registry/befitness/",
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
        "url": "https://api.github.com/repos/brian91292/SyncSaber/releases/latest", 
        "enabled": True,
        "type": "brian91292_dll",
        "destination": "./Plugins/SyncSaber.dll",
    }
]

class mod:
    def install(mod):
        if mod['enabled'] == True:
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
                with open(dll_dest, 'wb') as F:
                    F.write(dll_contents)

class ipa:
    def install():
        if os.name != 'nt':
            os.environ['WINEPREFIX'] = os.path.realpath('../../compatdata/620980/pfx/')
            subprocess.run('wine ./IPA.exe "Beat Saber.exe"', shell=True)
        else:
            subprocess.run('IPA.exe "Beat Saber.exe"', shell=True)

if __name__ == '__main__':
    if os.getcwd().split(os.sep)[-1] != "Beat Saber":
        exit("Please run this from the Beat Saber directory")

    if not os.path.isdir('./UserData'):
        os.mkdir('./UserData')

    for item in mods:
        mod.install(item)

    if os.path.isdir('./IPA/Backups') and len(os.listdir('IPA/Backups/Beat Saber')) != 0:
        print("IPA.exe has already been run. Skipping.")
    else:
        ipa.install()

    print("Mods installed successfully!")
