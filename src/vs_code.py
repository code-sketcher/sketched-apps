import subprocess
from src.abstract_app import AbstractApp
from src.app import App

class VSCode(AbstractApp):
  def __init__(self):
    super().__init__('code')

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
      self.notify.error(f"Failed to install VS Code. Error: {e}")

  def __install_apt(self):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
    
    if self.installation_method != 'apt':
      return;

    dependency_app = App('curl', is_dependency=True)
    dependency_app.install()

    self.notify.print_info(f"Start vs code config on Debian based systems!")

    # Fetch the Microsoft GPG key and save it as microsoft.gpg
    fetch_gpg_key_command = 'curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg'
    subprocess.run(fetch_gpg_key_command, check=True, shell=True)

    # Install the GPG key to the system's keyring
    install_gpg_key_command = 'sudo install -o root -g root -m 644 microsoft.gpg /usr/share/keyrings/microsoft-archive-keyring.gpg'
    subprocess.run(install_gpg_key_command, check=True, shell=True)
    
    # Add the Visual Studio Code repository configuration
    config_repo = 'sudo sh -c \'echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list\''
    subprocess.run(config_repo, check=True, shell=True)

    super().install()

    subprocess.run('rm microsoft.gpg', check=True, shell=True)
