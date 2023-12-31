import subprocess
from src.abstract_app import AbstractApp
from src.app import App


class Brave(AbstractApp):
    def __init__(self):
        super().__init__('brave-browser')

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
            self.notify.error(f"Failed to install brave-browser. Error: {e}")

    def __install_apt(self):
        if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
            return

        if self.installation_method != 'apt':
            return;

        dependency_app = App('curl', is_dependency=True)
        dependency_app.install()

        self.notify.print_info(f"Start brave-browser config on Debian based systems!")

        fetch_gpg_key_command = 'sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg'
        subprocess.run(fetch_gpg_key_command, check=True, shell=True)

        config_repo = 'echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list'
        subprocess.run(config_repo, check=True, shell=True)

        super().install()
