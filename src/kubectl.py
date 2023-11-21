import subprocess
from src.abstract_app import AbstractApp
from src.app import App

class Kubectl(AbstractApp):
  def __init__(self):
    super().__init__('kubectl', installation_method = 'other')

  def install(self):
    if self.is_installed():
      self.notify.print_info(f"{self.name} is already installed.")
      ## if it is a dependency I don't want to add it as already installed app
      self.already_installed = not self.is_dependency
      
      return
    
    try:
      self.__install_other()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install kubectl. Error: {e}")
      return
    
    if self.is_installed():
      self.notify.print_success(f"Kubectl installed successfully!")
      self.installed = True

  def __install_other(self):
    dependency_app = App('curl', is_dependency=True)
    dependency_app.install()

    self.notify.print_info(f"Start kubectl installation!")
    
    download_release_command = 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"'
    subprocess.run(download_release_command, check=True, shell=True)

    download_checksum_file_command = 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"'
    subprocess.run(download_checksum_file_command, check=True, shell=True)

    validate_against_checksum_command = 'echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check'
    subprocess.run(validate_against_checksum_command, check=True, shell=True)

    install_command = 'sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl'
    subprocess.run(install_command, check=True, shell=True)

    subprocess.run('rm kubectl', check=True, shell=True)
    subprocess.run('rm kubectl.sha256', check=True, shell=True)
