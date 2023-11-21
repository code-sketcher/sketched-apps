import subprocess
from src.abstract_app import AbstractApp

class Onlyoffice(AbstractApp):
  def __init__(self):
    super().__init__('onlyoffice-desktopeditors')

  def install(self):
    if self.is_installed():
      self.notify.print_info(f"{self.name} is already installed.")
      ## if it is a dependency I don't want to add it as already installed app
      self.already_installed = not self.is_dependency

      return

    try:
      self.__install_apt()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install onlyoffice-desktopeditors. Error: {e}")
      self.installed = False

  def __install_apt(self):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return

    if self.installation_method != 'apt':
      return;

    self.notify.print_info(f"Start kubectl installation!")
    
    keyring_command = 'gpg --no-default-keyring --keyring gnupg-ring:/tmp/onlyoffice.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys CB2DE8E5'
    subprocess.run(keyring_command, check=True, shell=True)

    set_permissions_command = 'chmod 644 /tmp/onlyoffice.gpg'
    subprocess.run(set_permissions_command, check=True, shell=True)

    change_user_and_group_command = 'sudo chown root:root /tmp/onlyoffice.gpg'
    subprocess.run(change_user_and_group_command, check=True, shell=True)

    add_repo_command = 'echo \'deb [signed-by=/usr/share/keyrings/onlyoffice.gpg] https://download.onlyoffice.com/repo/debian squeeze main\' | sudo tee -a /etc/apt/sources.list.d/onlyoffice.list'
    subprocess.run(add_repo_command, check=True, shell=True)

    super().install()

