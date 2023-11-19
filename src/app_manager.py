import subprocess
import shutil
from src.notifier import Notifier
from src.distribution import Distribution

class AppManager:
  def __init__(self): 
    self.notify = Notifier()
    distribution = Distribution()
    self.distribution_name = distribution.get_name()

  def is_installed(self, app_name):
    return shutil.which(app_name)

  def install(self, app_name):
    if self.is_installed(app_name):
      self.notify.warning(f"{app_name} is already installed.")
      return

    self.__install_with_apt(app_name)

    if is_installed(app_name):
      self.notify.success(f"{app_name} has been installed successfully.")
      return
    
    self.notify.error(f"Please check if {app_name} has been installed. Looks like was not!")

  def __install_with_apt(self, app_name):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
    
    package_manager = 'apt'
    if self.is_installed('nala'):
      package_manager = 'nala'
    try:
      subprocess.run(['sudo', package_manager, 'install', '-y', app_name], check=True)
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install {app_name}. Error: {e}")
      
