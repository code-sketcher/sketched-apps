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
from src.chrome import Chrome
from src.vim import Vim
from src.vim import Nvim
from src.distribution import Distribution


class AppList:
    def __init__(self):
        self.distribution_name = Distribution().get_name()
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
            self.notify.print_success(" ".join(self.installed))

        total_already_installed = len(self.already_installed)
        if total_already_installed > 0:
            self.notify.print_warning(
                f"{total_already_installed} already installed apps!"
            )
            self.notify.print_warning(" ".join(self.already_installed))

        total_failed = len(self.failed)
        if total_failed > 0:
            self.notify.print_error(f"{total_failed} failed apps!")
            self.notify.print_error(" ".join(self.failed))

        total_dependencies = len(self.installed_as_dependencies)
        if total_dependencies > 0:
            self.notify.print_warning(
                f"{total_dependencies} apps installed as dependency!"
            )
            self.notify.print_warning(" ".join(self.installed_as_dependencies))

    def __get_apps(self):
        if self.distribution_name == "Debian" or self.distribution_name == "Ubuntu":
            return self.__get_ubuntu_debian_apps()

        if self.distribution_name == "OpenSUSE":
            return self.__get_opensuse_apps()

        if self.distribution_name == "Pop":
            return self.__get_pop_apps()

        return []

    def __get_pop_apps(self):
        return [
            App("nala"),
            App("curl"),
            App("make"),
            App("cmake"),
            App("rsync"),
            App("fastfetch"),
            App("fd-find"),
            App("fzf"),
            App("mc"),
            App("htop"),
            App("btop"),
            App("rsync"),
            App("bat"),
            Vim(),
            Nvim(),
            Onlyoffice(),
            VSCode(),
            JetbrainsToolbox(),
            Chrome(),
            BeekeeperStudio(),
            Kitty(),
            Kubectl(),
            Docker(),
            Brave(),
        ]

    def __get_opensuse_apps(self):
        return [
            App("opi", installation_method="zypper"),
            App("curl", installation_method="zypper"),
            App("fastfetch", installation_method="zypper"),
            App("autojump", installation_method="zypper"),
            App("fzf", installation_method="zypper"),
            App(
                "fd", installation_method="zypper"
            ),  # a tool like find is used for telescope nvim also
            App(
                "ripgrep", name_to_check="rg", installation_method="zypper"
            ),  # used for telescope nvim
            App("lazygit", installation_method="zypper"),  # used also for lazy nvim
            App("mc", installation_method="zypper"),
            App("tmux", installation_method="zypper"),
            App("bat", installation_method="zypper"),
            App("zoxide", installation_method="zypper"),
            App("zellij", installation_method="zypper"),
            App("zellij-bash-completion", installation_method="zypper"),
            App("flameshot", installation_method="zypper"),
            App("htop", installation_method="zypper"),
            App("btop", installation_method="zypper"),
            App("nvim", installation_method="zypper"),
            App("rsync", installation_method="zypper"),
            App("wtype", installation_method="zypper"),
            App("rofi-wayland", name_to_check="rofi", installation_method="zypper"),
            App("pass-otp", installation_method="zypper"),
            App("kitty", installation_method="zypper"),
            App("discord", installation_method="zypper"),
            App(
                "ca-certificates-steamtricks", installation_method="zypper"
            ),  # needed for steam games
            App("steam", installation_method="zypper"),
            App("docker", installation_method="zypper"),
            App("docker-compose", installation_method="zypper"),
            App("docker-compose-switch", installation_method="zypper"),
            App("docker-buildx", installation_method="zypper"),
            App(
                "libvirt", installation_method="zypper"
            ),  # dependency for qemu, note that you will need to start the daemon libvirtd
            App("qemu", installation_method="zypper"),
            App("virt-manager", installation_method="zypper"),
            Brave(installation_method="zypper"),
            Chrome("google-chrome-stable", installation_method="zypper"),
            VSCode(installation_method="zypper"),
            JetbrainsToolbox(),
            Kubectl(),
            Postman(),
            App("spotify", installation_method="snap"),
            App(
                "notion-snap-reborn", name_to_check="notion", installation_method="snap"
            ),
        ]

    def __get_ubuntu_debian_apps(self):
        return [
            App("nala"),
            App("curl"),
            App("vim"),
            App("autojump"),
            App("mc"),
            App("cmake"),
            App("rsync"),
            App("autojump"),
            App("libfuse2"),  # dependency for app images
            # App('preload'),
            App("fastfetch"),
            App("flameshot"),
            App("gpick"),
            App("gimp"),
            App("dconf-editor"),
            App("network-manager-openconnect-gnome", "openconnect"),
            App("gnome-tweaks"),
            App("gnome-shell-extensions", "gnome-extensions-app"),
            App("gnome-shell-extension-manager", "extension-manager"),
            App("btop"),
            App("htop"),
            App("caffeine"),
            App("spotify", installation_method="snap"),
            App("notesnook", installation_method="snap"),
            App("discord", installation_method="snap"),
            Onlyoffice(),
            VSCode(),
            Kubectl(),
            Docker(),
            BeekeeperStudio(),
            Kitty(),
            Ulauncher(),
            Brave(),
            Postman(),
            JetbrainsToolbox(),
            Chrome(),
        ]
