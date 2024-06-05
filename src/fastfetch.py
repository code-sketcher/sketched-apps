import subprocess
from src.abstract_app import AbstractApp


class Ulauncher(AbstractApp):
    def __init__(self):
        super().__init__("fastfetch")

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
            self.notify.error(f"Failed to install Fastfetch. Error: {e}")

    def __install_apt(self):
        if self.installation_method != "apt":
            return

        if (
            self.distribution_name != "Debian"
            and self.distribution_name != "Ubuntu"
            and self.distribution_name != "Pop"
        ):
            return

        if self.distribution_name == "Ubuntu" or self.distribution_name == "Pop":
            subprocess.run(
                "sudo add-apt-repository ppa:zhangsongcui3371/fastfetch -y",
                check=True,
                shell=True,
            )

            super().install()

            return

        if self.distribution_name != "Debian":
            return
