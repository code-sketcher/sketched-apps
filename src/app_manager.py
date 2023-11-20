import subprocess
import shutil
from src.notifier import Notifier
from src.distribution import Distribution

class AppManager:
  def __init__(self): 
    self.notify = Notifier()
    distribution = Distribution()
    self.distribution_name = distribution.get_name()

    self.__set_apt_manager()

  def is_installed(self, app_name):
    return shutil.which(app_name)

  def install(self, app_name):
    if self.is_installed(app_name):
      self.notify.warning(f"{app_name} is already installed.")
      return

    self.notify.print_info(f"Start {app_name} installation!")

    self.__install_with_apt(app_name)

    if self.is_installed(app_name):
      self.notify.success(f"{app_name} has been installed successfully.")
      return
    
    self.notify.error(f"Please check if {app_name} has been installed. Looks like was not!")

  def install_by_approval(self, app_name, user_info):
    if self.is_installed(app_name):
        return True
    
    self.notify.print_info(f"{user_info}")
    user_input = input(f"Do you want to install it? (y/n): ").lower()
    
    if user_input != 'y':
      return False

    self.install(app_name)

    return True

  def __install_with_apt(self, app_name):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
    
    try:
      subprocess.run(['sudo', self.apt_manager, 'update'], check=True)
      subprocess.run(['sudo', self.apt_manager, 'install', '-y', app_name], check=True)
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install {app_name}. Error: {e}")

  def __set_apt_manager(self):
    self.apt_manager = 'apt'
    if self.is_installed('nala'):
      self.apt_manager = 'nala'
      return
    
    if self.install_by_approval('nala', 'Nala is not installed! Is used for pretty printing.'):
      self.apt_manager = 'nala'
