import subprocess
from src.distribution import Distribution
from src.app_manager import AppManager
from src.notifier import Notifier

class VSCode:
  def __init__(self):
    self.notify = Notifier()

    distribution = Distribution()
    self.distribution_name = distribution.get_name()
    
    self.app = AppManager()

  def install(self):
    if self.app.is_installed('code'):
      return

    try:
      self.__install_apt()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install VS Code. Error: {e}")

  def __install_apt(self):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
    
    if not self.app.install_by_approval('curl', 'Curl is a dependency for VS Code!'):
      return

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

    self.app.install('code')

    subprocess.run('rm microsoft.gpg', check=True, shell=True)
