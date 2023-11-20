import subprocess
from src.distribution import Distribution
from src.app_manager import AppManager
from src.notifier import Notifier

class Docker:
  def __init__(self):
    self.notify = Notifier()

    distribution = Distribution()
    self.distribution_name = distribution.get_name()
    
    self.app = AppManager()

  def install(self):
    if self.app.is_installed('docker'):
      return

    try:
      self.__install_apt()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install docker. Error: {e}")

  def __install_apt(self):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
    
    if not self.app.install_by_approval('curl', 'Curl is a dependency for VS Code!'):
      return

    self.notify.print_info(f"Start docker config on Debian based systems!")
    
    if self.distribution_name == 'Ubuntu':
      get_gpg_key_command='curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg'

    if self.distribution_name == 'Debian':
      get_gpg_key_command='curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg'

    subprocess.run(get_gpg_key_command, check=True, shell=True)

    subprocess.run(
      'echo \
        "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
      check=True,
      shell=True
    )
    
    install_command = 'sudo nala install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin'
    subprocess.run(install_command, check=True, shell=True)
    
    if self.app.is_installed('docker'):
      self.notify.success(f"Docker installed successfully!")
