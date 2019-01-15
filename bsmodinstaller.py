#!/usr/bin/env python
import abc
import json,requests,os,subprocess
from io import BytesIO
from zipfile import ZipFile

class mod_installer(abc.ABCMeta):
    def __new__(cls, install_data):
        if cls is mod_installer:
            installer_type = install_data.get('type')
            if installer_type == 'modsaber':
                return super(mod_installer, cls).__new__(modsaber)
            if installer_type == 'brian91292_dll':
                return super(mod_installer, cls).__new__(brian91292_dll)
        else:
            return super(mod_installer, cls).__new__(cls, install_data)

    def __init__(self, install_data):
        self.install_data = install_data
        if self.check_if_enabled() == True:
            self.install()
        elif self.check_if_enabled() == False:
            if self.check_if_installed():
                self.uninstall()

    def check_if_enabled(self):
        enabled = install_data.get('enabled', None)
        if enabled == True:
            return True
        if isinstance(enabled, basestring):
            enabled = enabled.lower()
            if enabled == 'true':
                return True
            elif enabled == 'false':
                return False
            else:
                return None

    def check_if_installed(self):
        '''Method for checking if something is installed
        Expected returns are True for installed and False for not installed
        When not overwritten by a subclass default to not installed'''
        return False

    @abc.abstractmethod
    def install(self):
        '''Required abstract method for performing an install'''
        pass

    def uninstall(self):
        '''Method for removing a given mod'''
        pass

class modsaber(mod_installer):
    def install(self):
        modsaber_url = self.install_data.get('url')
        mod_name = self.install_data.get('name')
        print('Installing %s from modsaber...' %(mod_name))
        modsaber_meta_data = requests.get(modsaber_url).json()
        zip_url = modsaber_meta_data.get('files', {}).get('steam', {}).get('url')
        zip_data = BytesIO(requests.get(zip_url).content)
        ZipFile(zip_data).extractall()
        print('Installation of %s complete' %(mod_name))

class brian91292_dll(mod_installer):
    def install(self):
        metadata_url = self.install_data.get('url')
        dll_dest = self.install_data.get('destination')
        mod_name = self.install_data.get('name')
        print('Installing %s to %s...' %(mod_name, dll_dest))
        metadata = requests.get(metadata_url).json()
        dll_url = metadata.get('assets', [])[0].get("browser_download_url")
        dll_contents = requests.get(dll_url).content
        with open(dll_dest, 'wb') as F:
            F.write(dll_contents)

    def uninstall(self):
        dll_dest = self.install_data.get('destination')
        os.remove(dll_dest)

    def check_if_installed(self):
        dll_dest = self.install_data.get('destination')
        return os.path.isfile(dll_dest) 


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
    "name": "customui",
    "url": "https://www.modsaber.org/registry/customui/", 
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

if __name__ == '__main__':
    if os.getcwd().split(os.sep)[-1] != "Beat Saber":
        sys.exit("Please run this from the Beat Saber directory")

    if not os.path.isdir('./UserData'):
        os.mkdir('./UserData')

    for mod in mods:
        try:
            mod_installer(install_data=mod)
        except Exception as E:
            print('Ran into an issue wile installing the following mod:\n %s' %(mod))
            print('Error that as encountered was:')
            print(E)

    prefix = os.path.realpath('../../compatdata/620980/pfx/')
    os.environ['WINEPREFIX'] = prefix
    subprocess.run('wine ./IPA.exe "Beat Saber.exe"', shell=True)
