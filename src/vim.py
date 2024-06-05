import subprocess
from src.abstract_app import AbstractApp
from src.app import App


class Vim(AbstractApp):
    def __init__(self):
        super().__init__("vim", installation_method="other")

    def install(self):
        if self.is_installed():
            self.notify.print_info(f"{self.name} is already installed.")
            self.already_installed = not self.is_dependency

            return

        try:
            self.__install_apt()
        except subprocess.CalledProcessError as e:
            self.notify.error(f"Failed to install vim from source. Error: {e}")
            return

        if self.is_installed():
            self.notify.print_success(f"vim from source installed successfully!")
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

        self.notify.print_info(
            f"Start installing vim dependencies on debian based system!"
        )

        make_dependency = App("make", is_dependency=True)
        make_dependency.install()

        clang_dependency = App("clang", is_dependency=True)
        clang_dependency.install()

        libtool_dependency = App("libtool-bin", is_dependency=True)
        libtool_dependency.install()

        libxt_dependency = App("libxt-dev", is_dependency=True)
        libxt_dependency.install()

        libgtk_dependency = App("libgtk-3-dev", is_dependency=True)
        libgtk_dependency.install()

        self.__install_from_source()

    def __install_from_source(self):
        self.notify.print_info(f"Start compiling vim from source!")

        subprocess.run(
            "git clone https://github.com/vim/vim.git ~/.local/apps/source/vim",
            check=True,
            shell=True,
        )
        subprocess.run("make -C ~/.local/apps/source/vim/src", check=True, shell=True)
        subprocess.run(
            "sudo make install -C ~/.local/apps/source/vim/src", check=True, shell=True
        )
