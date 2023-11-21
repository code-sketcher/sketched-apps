from src.app import App
from src.onlyoffice import Onlyoffice
from src.vs_code import VSCode
from src.kubectl import Kubectl
from src.docker import Docker
from src.beekeeper_studio import BeekeeperStudio

class AppList:
    def __init__(self):
      self.apps = self.__get_apps()
      self.already_installed = [];
      self.installed = [];
      self.failed = [];
      self.installed_as_dependencies = [];
        
    
    def install_list(self):
      for app in self.apps:
        app.install();
        if app.already_installed:
          self.already_installed.append(app.name)
          continue
        if app.installed:
          self.installed.append(app.name)
          continue

        self.failed.append(app.name)

        if app.is_dependency and not app.install and not app.already_installed:
           self.installed_as_dependencies.append(app.name)

    def __get_apps(self):
      return [
        App('nala'),
        App('curl'),
        App('vim'),
        App('rsync'),
        #App('libfuse2'), #dependency for app images
        App('preload'),
        App('neofetch'),
        App('flameshot'),
        App('gpick'),
        App('gimp'),
        App('dconf-editor'),
        App('network-manager-openconnect-gnome', 'openconnect'),
        App('gnome-tweaks'),
        App('gnome-shell-extensions', 'gnome-extensions-app'),
        App('gnome-shell-extension-manager', 'extension-manager'),
        App('btop'),
        App('htop'),
        App('caffeine'),
        App('spotify', installation_method = 'snap'),
        App('notesnook', installation_method = 'snap'),
        App('discord', installation_method = 'snap'),
        Onlyoffice(),
        VSCode(),
        Kubectl(),
        Docker(),
        BeekeeperStudio()
      ]