import subprocess
from src.distribution import Distribution
from src.app_manager import AppManager
from src.notifier import Notifier

class BeekeeperStudio:
  def __init__(self):
    self.notify = Notifier()

    distribution = Distribution()
    self.distribution_name = distribution.get_name()
    
    self.app = AppManager()

  def install(self):
    if self.app.is_installed("/opt/Beekeeper Studio/beekeeper-studio"):
      return

    try:
      self.__install_apt()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install Beekeeper. Error: {e}")

  def __install_apt(self):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
   
    if not self.app.install_by_approval('curl', 'Curl is a dependency for Beekeeper Studio!'):
      return

    self.notify.print_info(f"Start beekeeper config on Debian based systems!")

    # Install the GPG key to the system's keyring
    install_gpg_key_command = 'curl -fSsl https://deb.beekeeperstudio.io/beekeeper.key | gpg --dearmor | sudo tee /usr/share/keyrings/beekeeper.gpg > /dev/null'
    subprocess.run(install_gpg_key_command, check=True, shell=True)
    
    # Add the Visual Studio Code repository configuration
    config_repo = 'echo \'deb [signed-by=/usr/share/keyrings/beekeeper.gpg] https://deb.beekeeperstudio.io stable main\' | sudo tee /etc/apt/sources.list.d/beekeeper-studio-app.list'
    subprocess.run(config_repo, check=True, shell=True)

    self.app.install('beekeeper-studio')
