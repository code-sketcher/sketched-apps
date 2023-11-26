from src.app import App
from src.onlyoffice import Onlyoffice
from src.vs_code import VSCode
from src.kubectl import Kubectl
from src.docker import Docker
from src.beekeeper_studio import BeekeeperStudio
from src.notifier import Notifier
from src.kitty import Kitty
from src.ulauncher import Ulauncher
from src.brave import Brave
from src.postman import Postman
from src.jetbrains_toolbox import JetbrainsToolbox


class AppList:
    def __init__(self):
        self.apps = self.__get_apps()
        self.already_installed = []
        self.installed = []
        self.failed = []
        self.installed_as_dependencies = []

        self.notify = Notifier()

    def install(self):
        for app in self.apps:
            app.install()
            if app.already_installed:
                self.already_installed.append(app.name)
                continue
            if app.installed:
                self.installed.append(app.name)
                continue

            self.failed.append(app.name)

            if app.is_dependency and not app.install and not app.already_installed:
                self.installed_as_dependencies.append(app.name)

    def display_results(self):
        total_installed_apps = len(self.installed)
        if total_installed_apps > 0:
            self.notify.print_success(f"{total_installed_apps} installed apps!")
            self.notify.print_success(' '.join(self.installed))

        total_already_installed = len(self.already_installed)
        if total_already_installed > 0:
            self.notify.print_warning(f"{total_already_installed} already installed apps!")
            self.notify.print_warning(' '.join(self.already_installed))

        total_failed = len(self.failed)
        if total_failed > 0:
            self.notify.print_error(f"{total_failed} failed apps!")
            self.notify.print_error(' '.join(self.failed))

        total_dependencies = len(self.installed_as_dependencies)
        if total_dependencies > 0:
            self.notify.print_warning(f"{total_dependencies} apps installed as dependency!")
            self.notify.print_warning(' '.join(self.installed_as_dependencies))

    def __get_apps(self):
        return [
            App('nala'),
            App('curl'),
            App('vim'),
            App('mc'),
            App('cmake'),
            App('rsync'),
            App('libfuse2'),  # dependency for app images
            #App('preload'),
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
            App('spotify', installation_method='snap'),
            App('notesnook', installation_method='snap'),
            App('discord', installation_method='snap'),
            Onlyoffice(),
            VSCode(),
            Kubectl(),
            Docker(),
            BeekeeperStudio(),
            Kitty(),
            Ulauncher(),
            Brave(),
            Postman(),
            JetbrainsToolbox()
        ]
