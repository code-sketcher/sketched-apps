import subprocess
import shutil
from abc import ABC, abstractmethod
from src.notifier import Notifier
from src.distribution import Distribution

class AbstractApp(ABC):
  def __init__(
      self, 
      name, 
      name_to_check = '', 
      installation_method = 'apt', 
      is_dependency = False
    ):
    self.name = name
    self.name_to_check = name_to_check
    if not self.name_to_check: 
      self.name_to_check = self.name
    
    self.is_dependency = is_dependency
    self.installation_method = installation_method
    self.installed = False
    self.already_installed = False

    self.notify = Notifier()
    self.distribution = Distribution()
    self.distribution_name = self.distribution.get_name()

  @abstractmethod
  def install(self):
    if self.is_installed():
      self.notify.print_info(f"{self.name} is already installed.")
      
      ## if it is a dependency I don't want to add it as already installed app
      self.already_installed = not self.is_dependency 

      return
    
    dependency_text = ''
    if self.is_dependency:
      dependency_text = ' as dependency'

    self.notify.print_info(f"Start {self.name} installation{dependency_text}!")

    self.__install_with_apt()
    self.__install_snap()
    self.__check_installation()

  def is_installed(self):
    return shutil.which(self.name_to_check)

  def __check_installation(self):
    if self.is_installed():
      self.installed = True
      self.notify.print_success(f"{self.name} has been installed successfully.")
      return
    
    self.notify.error(f"Please check if {self.name} has been installed. Looks like was not!")

  def __install_snap(self):
    if self.installation_method != 'snap':
      return;

    try:
      subprocess.run(['sudo', 'snap', 'install', self.name], check=True)
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install {self.name}. Error: {e}")

  def __install_with_apt(self):
    if self.distribution_name != 'Debian' and self.distribution_name != 'Ubuntu':
      return
    
    if self.installation_method != 'apt':
      return;

    try:
      apt_manager = self.__get_apt_manager()
      subprocess.run(['sudo', apt_manager, 'update'], check=True)
      subprocess.run(['sudo', apt_manager, 'install', '-y', self.name], check=True)
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install {self.name}. Error: {e}")

  def __get_apt_manager(self):
    apt_manager = 'apt'
    if  shutil.which('nala'):
      apt_manager = 'nala'
    
    return apt_manager