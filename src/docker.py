import subprocess
from src.abstract_app import AbstractApp
from src.app import App

class Docker(AbstractApp):
  def __init__(self):
    super().__init__('docker')

  def install(self):
    if self.is_installed():
      self.notify.print_info(f"{self.name} is already installed.")
      ## if it is a dependency I don't want to add it as already installed app
      self.already_installed = not self.is_dependency
      
      return
    
    try:
      self.__install_apt()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install docker. Error: {e}")
    
    if self.is_installed():
      self.notify.print_success(f"Docker installed successfully!")
      self.installed = True

  def __install_apt(self):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
    
    if self.installation_method != 'apt':
      return;
  
    dependency_app = App('curl', is_dependency=True)
    dependency_app.install()

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
    
    install_command = 'sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin'
    subprocess.run(install_command, check=True, shell=True)
