import subprocess
from src.distribution import Distribution
from src.app_manager import AppManager
from src.notifier import Notifier

class Kubectl:
  def __init__(self):
    self.notify = Notifier()

    distribution = Distribution()
    self.distribution_name = distribution.get_name()
    
    self.app = AppManager()

  def install(self):
    if self.app.is_installed('kubectl'):
      return

    try:
      self.__install_all()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install kubectl. Error: {e}")

  def __install_all(self):
    if not self.app.install_by_approval('curl', 'Curl is a dependency for VS Code!'):
      return

    self.notify.print_info(f"Start kubectl installation!")
    
    download_release_command = 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"'
    subprocess.run(download_release_command, check=True, shell=True)

    download_checksum_file_command = 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"'
    subprocess.run(download_checksum_file_command, check=True, shell=True)

    validate_against_checksum_command = 'echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check'
    subprocess.run(validate_against_checksum_command, check=True, shell=True)

    install_command = 'sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl'
    subprocess.run(install_command, check=True, shell=True)
    
    if self.app.is_installed('kubectl'):
      self.notify.success(f"Kubectl installed successfully!")
      return
    
    self.notify.error(f"Kubectl not installed!")
