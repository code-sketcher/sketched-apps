import subprocess
from src.abstract_app import AbstractApp
from src.app import App


class Nvim(AbstractApp):
    def __init__(self):
        super().__init__("nvim")

    def install(self):
        if self.is_installed():
            self.notify.print_info(f"{self.name} is already installed.")
            self.already_installed = not self.is_dependency

            return

        try:
            self.__install_apt()
        except subprocess.CalledProcessError as e:
            self.notify.error(f"Failed to install nvim from source. Error: {e}")
            return

        if self.is_installed():
            self.notify.print_success(f"nvim from source installed successfully!")
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
            f"Start installing nvim dependencies on debian based system!"
        )

        clang_dependency = App("clang", is_dependency=True)
        clang_dependency.install()

        cmake_dependency = App("cmake", is_dependency=True)
        cmake_dependency.install()

        ninja_build_dependency = App("ninja-build", is_dependency=True)
        ninja_build_dependency.install()

        subprocess.run(["sudo", "apt", "install", "-y", "gettext"], check=True)

        unzip_dependency = App("unzip", is_dependency=True)
        unzip_dependency.install()

        curl_dependency = App("curl", is_dependency=True)
        curl_dependency.install()

        build_essential_dependency = App("build-essential", is_dependency=True)
        build_essential_dependency.install()

        self.__install_from_source()

    def __install_from_source(self):
        self.notify.print_info(f"Start compiling nvim from source!")

        subprocess.run(
            "git clone https://github.com/neovim/neovim ~/.local/apps/source/neovim",
            check=True,
            shell=True,
        )
        subprocess.run(
            "git --git-dir=$HOME/.local/apps/source/neovim/.git checkout stable -f",
            check=True,
            shell=True,
        )
        subprocess.run(
            "make CMAKE_BUILD_TYPE=RelWithDebInfo -C ~/.local/apps/source/neovim",
            check=True,
            shell=True,
        )
        subprocess.run(
            "cpack -B ~/.local/apps/source/neovim/build -G DEB && sudo dpkg -i ~/.local/apps/source/neovim/build/nvim-linux64.deb",
            check=True,
            shell=True,
        )
