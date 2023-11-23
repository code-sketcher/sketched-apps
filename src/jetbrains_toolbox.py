import subprocess
import requests
import os
from src.abstract_app import AbstractApp
from src.app import App


class JetbrainsToolbox(AbstractApp):
    def __init__(self):
        super().__init__('jetbrains-toolbox', installation_method='other')

    def install(self):
        if self.__is_installed():
            self.notify.print_info(f"{self.name} is already installed.")
            self.already_installed = not self.is_dependency

            return

        try:
            self.__install_other()
        except subprocess.CalledProcessError as e:
            self.notify.error(f"Failed to install jetbrains-toolbox. Error: {e}")
            return

        if self.__is_installed():
            self.notify.print_success(f"jetbrains-toolbox installed successfully!")
            self.installed = True

    def __is_installed(self):
        home_path = os.path.expanduser("~")
        app_path = os.path.join(home_path, '.local/bin/jetbrains-toolbox')

        if not os.path.isfile(app_path):
            return False

        try:
            subprocess.run([app_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def __get_download_url(self):
        url = 'https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release'
        response = requests.get(url)
        response.raise_for_status()

        json_data = response.json()

        tba_list = json_data.get('TBA')

        if isinstance(tba_list, list) and tba_list:
            return tba_list[0].get('downloads', {}).get('linux', {}).get('link')

    def __install_other(self):
        dependency_app = App('curl', is_dependency=True)
        dependency_app.install()

        self.notify.print_info(f"Start jetbrains-toolbox installation!")

        try:
            download_url = self.__get_download_url()
        except requests.RequestException as e:
            self.notify.print_error(f"Error fetching data: {e}")
            return

        subprocess.run('sudo rm -rf /tmp/jetbrains-*', check=True, shell=True)

        create_bin_folder_command = 'mkdir -p ~/.local/bin'
        subprocess.run(create_bin_folder_command, check=True, shell=True)
        extract_command = f'tar -C /tmp/ -xzf <(curl -L {download_url}) --strip-components=1'
        subprocess.run(['bash', '-c', extract_command], check=True)
        create_target_folder_command = 'mkdir -p /home/$USER/.local/share/JetBrains/Toolbox/bin'
        subprocess.run(create_target_folder_command, check=True, shell=True)
        subprocess.run(
            f'sudo mv /tmp/jetbrains-toolbox /home/$USER/.local/share/JetBrains/Toolbox/bin/jetbrains-toolbox',
            check=True, shell=True)

        create_symlink_command = 'ln -sf /home/$USER/.local/share/JetBrains/Toolbox/bin/jetbrains-toolbox ~/.local/bin/jetbrains-toolbox'
        subprocess.run(create_symlink_command, check=True, shell=True)
