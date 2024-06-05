import subprocess
from src.abstract_app import AbstractApp
from src.app import App


class Chrome(AbstractApp):
    def __init__(self, name="google-chrome", installation_method="apt"):
        super().__init__(name, installation_method=installation_method)

        self.should_update = True

    def install(self):
        if self.is_installed():
            self.notify.print_info(f"{self.name} is already installed.")
            ## if it is a dependency I don't want to add it as already installed app
            self.already_installed = not self.is_dependency

            return

        try:
            self.__install_apt()
            self.__install_zypper()
        except subprocess.CalledProcessError as e:
            self.notify.error(f"Failed to install Google Chrome. Error: {e}")

        if self.is_installed():
            self.notify.print_success(f"Google Chrome installed successfully!")
            self.installed = True

    def __install_apt(self):
        if (
            self.distribution_name != "Debian"
            and self.distribution_name != "Ubuntu"
            and self.distribution_name != "Pop"
        ):
            return

        if self.installation_method != "apt":
            return

        dependency_app = App("curl", is_dependency=True)
        dependency_app.install()

        self.notify.print_info(f"Start google-chrome config on Debian based systems!")

        download_command = "sudo curl -o /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
        subprocess.run(download_command, check=True, shell=True)

        install_command = (
            "sudo apt install /tmp/google-chrome-stable_current_amd64.deb -y"
        )
        subprocess.run(install_command, check=True, shell=True)

    def __install_zypper(self):
        if self.distribution_name != "OpenSUSE" or self.installation_method != "zypper":
            return

        self.notify.print_info(f"Start google-chrome-stable config on OpenSUSE!")

        import_key_command = (
            "sudo rpm --import https://dl-ssl.google.com/linux/linux_signing_key.pub"
        )
        subprocess.run(import_key_command, check=True, shell=True)

        add_repo_command = "sudo zypper addrepo http://dl.google.com/linux/chrome/rpm/stable/x86_64 Google-Chrome"
        subprocess.run(add_repo_command, check=True, shell=True)

        super().install()
