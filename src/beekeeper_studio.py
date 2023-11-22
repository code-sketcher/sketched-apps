import subprocess
from src.abstract_app import AbstractApp
from src.app import App

class BeekeeperStudio(AbstractApp):
  def __init__(self):
    super().__init__('beekeeper-studio', "/opt/Beekeeper Studio/beekeeper-studio")

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
      self.notify.error(f"Failed to install Beekeeper. Error: {e}")

  def __install_apt(self):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return

    if self.installation_method != 'apt':
      return;
  
    dependency_app = App('curl', is_dependency=True)
    dependency_app.install()

    self.notify.print_info(f"Start beekeeper config on Debian based systems!")

    # Install the GPG key to the system's keyring
    install_gpg_key_command = 'curl -fSsl https://deb.beekeeperstudio.io/beekeeper.key | gpg --dearmor | sudo tee /usr/share/keyrings/beekeeper.gpg > /dev/null'
    subprocess.run(install_gpg_key_command, check=True, shell=True)
    
    # Add the Visual Studio Code repository configuration
    config_repo = 'echo \'deb [signed-by=/usr/share/keyrings/beekeeper.gpg] https://deb.beekeeperstudio.io stable main\' | sudo tee /etc/apt/sources.list.d/beekeeper-studio-app.list'
    subprocess.run(config_repo, check=True, shell=True)

    super().install()
