#!/usr/bin/python
import json,requests,os,subprocess
from io import BytesIO
from zipfile import ZipFile

if os.getcwd().split(os.sep)[-1] != "Beat Saber":
    sys.exit("Please run this from the Beat Saber directory")

if not os.path.isdir('./UserData'):
    os.mkdir('./UserData')

#Song loader
songloader = requests.get("https://www.modsaber.org/registry/song-loader/")
ZipFile(BytesIO(requests.get(songloader.json()['files']['steam']['url']).content)).extractall()

#Song Browser
songbrowser = requests.get("https://www.modsaber.org/registry/songbrowserplugin")
ZipFile(BytesIO(requests.get(songbrowser.json()['files']['steam']['url']).content)).extractall()

#syncsaber
syncsaber = requests.get("https://api.github.com/repos/brian91292/SyncSaber/releases/latest")
with open('./Plugins/SyncSaber.dll', 'wb') as f:
    f.write(requests.get(syncsaber.json()['assets'][0]["browser_download_url"]).content)

#Libraries!
#CustomUI
customui = requests.get("https://www.modsaber.org/registry/customui/")
ZipFile(BytesIO(requests.get(customui.json()['files']['steam']['url']).content)).extractall()

#newtonsoft-json
nsjson = requests.get("https://www.modsaber.org/registry/newtonsoft-json")
ZipFile(BytesIO(requests.get(nsjson.json()['files']['steam']['url']).content)).extractall()

#harmony
harmony = requests.get("https://www.modsaber.org/registry/harmony")

prefix = os.path.realpath('../../compatdata/620980/pfx/')
os.environ['WINEPREFIX'] = prefix
subprocess.run('wine ./IPA.exe "Beat Saber.exe"', shell=True)
