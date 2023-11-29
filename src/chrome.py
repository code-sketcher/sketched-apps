import subprocess
from src.abstract_app import AbstractApp
from src.app import App


class Chrome(AbstractApp):
    def __init__(self):
        super().__init__('google-chrome')

        self.should_update = True

    def install(self):
        if self.is_installed():
            self.notify.print_info(f"{self.name} is already installed.")
            ## if it is a dependency I don't want to add it as already installed app
            self.already_installed = not self.is_dependency

            return

        try:
            self.__install_apt()
        except subprocess.CalledProcessError as e:
            self.notify.error(f"Failed to install Google Chrome. Error: {e}")

    def __install_apt(self):
        if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
            return

        if self.installation_method != 'apt':
            return;

        dependency_app = App('curl', is_dependency=True)
        dependency_app.install()

        self.notify.print_info(f"Start google-chrome config on Debian based systems!")

        download_command = 'sudo curl -o /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
        subprocess.run(download_command, check=True, shell=True)

        install_command = 'sudo apt install /tmp/google-chrome-stable_current_amd64.deb -y'
        subprocess.run(install_command, check=True, shell=True)
