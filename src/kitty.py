import subprocess
from src.abstract_app import AbstractApp
from src.app import App
import os


class Kitty(AbstractApp):
    def __init__(self):
        super().__init__('kitty', installation_method='other')

    def install(self):
        if self.is_kitty_installed():
            self.notify.print_info(f"{self.name} is already installed.")
            # if it is a dependency I don't want to add it as already installed app
            self.already_installed = not self.is_dependency

            return

        try:
            self.__install_other()
        except subprocess.CalledProcessError as e:
            self.notify.error(f"Failed to install kitty. Error: {e}")
            return

        if self.is_kitty_installed():
            self.notify.print_success(f"Kitty installed successfully!")
            self.installed = True

    def is_kitty_installed(self):
        home_path = os.path.expanduser("~")
        kitty_path = os.path.join(home_path, '.local/bin/kitty')

        if not os.path.isfile(kitty_path):
            return False

        try:
            subprocess.run([kitty_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def __install_other(self):
        dependency_app = App('curl', is_dependency=True)
        dependency_app.install()

        self.notify.print_info(f"Start kitty installation!")

        kitty_installer_command = 'curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin launch=n'
        subprocess.run(kitty_installer_command, check=True, shell=True)

        create_bin_folder_command = 'mkdir -p ~/.local/bin'
        subprocess.run(create_bin_folder_command, check=True, shell=True)

        add_kitty_to_path_command = 'ln -sf ~/.local/kitty.app/bin/kitty ~/.local/kitty.app/bin/kitten ~/.local/bin/'
        subprocess.run(add_kitty_to_path_command, check=True, shell=True)

        create_applications_folder_command = 'mkdir -p ~/.local/share/applications'
        subprocess.run(create_applications_folder_command, check=True, shell=True)

        place_kitty_desktop_command = 'cp ~/.local/kitty.app/share/applications/kitty.desktop ~/.local/share/applications/'
        subprocess.run(place_kitty_desktop_command, check=True, shell=True)

        place_kitty_open_desktop_command = 'cp ~/.local/kitty.app/share/applications/kitty-open.desktop ~/.local/share/applications/'
        subprocess.run(place_kitty_open_desktop_command, check=True, shell=True)

        add_kitty_icon_command = 'sed -i "s|Icon=kitty|Icon=/home/$USER/.local/kitty.app/share/icons/hicolor/256x256/apps/kitty.png|g" ~/.local/share/applications/kitty*.desktop'
        subprocess.run(add_kitty_icon_command, check=True, shell=True)

        update_kitty_path_command = 'sed -i "s|Exec=kitty|Exec=/home/$USER/.local/kitty.app/bin/kitty|g" ~/.local/share/applications/kitty*.desktop'
        subprocess.run(update_kitty_path_command, check=True, shell=True)
