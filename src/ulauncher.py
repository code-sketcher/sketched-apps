import subprocess
from src.abstract_app import AbstractApp
from src.app import App

class Ulauncher(AbstractApp):
  def __init__(self):
    super().__init__('ulauncher')

  def install(self):
    if self.is_installed():
      self.notify.print_info(f"{self.name} is already installed.")
      ## if it is a dependency I don't want to add it as already installed app
      self.already_installed = not self.is_dependency
      
      return
    
    try:
      self.__install_apt()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install Ulauncher. Error: {e}")

  def __install_apt(self):
    if self.installation_method != 'apt':
      return;
  
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
    
    if self.distribution_name == 'Ubuntu':
      subprocess.run('sudo add-apt-repository universe -y', check=True, shell=True)
      subprocess.run('sudo add-apt-repository ppa:agornostal/ulauncher-dev -y', check=True, shell=True)
      
      super().install()

      return

    if self.distribution_name != 'Debian':
      return

    self.notify.print_info(f"Start Ulauncher config on Debian based systems!")

    subprocess.run('gpg --keyserver keyserver.ubuntu.com --recv 0xfaf1020699503176', check=True, shell=True)

    install_gpg_key_command = 'gpg --export 0xfaf1020699503176 | sudo tee /usr/share/keyrings/ulauncher-archive-keyring.gpg > /dev/null'
    subprocess.run(install_gpg_key_command, check=True, shell=True)
    
    subprocess.run(
      'echo "deb [signed-by=/usr/share/keyrings/ulauncher-archive-keyring.gpg] \
          http://ppa.launchpad.net/agornostal/ulauncher-dev/ubuntu jammy main" \
          | sudo tee /etc/apt/sources.list.d/ulauncher-dev-jammy.list',
      check=True,
      shell=True
    )

    super().install()
