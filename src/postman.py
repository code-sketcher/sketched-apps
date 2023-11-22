import subprocess
from src.abstract_app import AbstractApp
from src.app import App

class Postman(AbstractApp):
  def __init__(self):
    super().__init__('postman', installation_method = 'other')

  def install(self):
    if self.is_installed():
      self.notify.print_info(f"{self.name} is already installed.")
      ## if it is a dependency I don't want to add it as already installed app
      self.already_installed = not self.is_dependency
      
      return
    
    try:
      self.__install_other()
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install postman. Error: {e}")
      return
    
    if self.is_installed():
      self.notify.print_success(f"Postman installed successfully!")
      self.installed = True

  def __install_other(self):
    dependency_app = App('curl', is_dependency=True)
    dependency_app.install()

    self.notify.print_info(f"Start postman installation!")
    
    create_bin_folder_command = 'mkdir -p ~/.local/bin'
    subprocess.run(create_bin_folder_command, check=True, shell=True)

    install_command = 'tar -C /tmp/ -xzf <(curl -L https://dl.pstmn.io/download/latest/linux_64) && sudo mv /tmp/postman /opt/'
    subprocess.run(install_command, check=True, shell=True)

    create_symlink_command = 'ln -sf /opt/postman/app/Postman ~/.local/bin/'
    subprocess.run(create_symlink_command, check=True, shell=True)

    create_applications_folder_command = 'mkdir -p ~/.local/share/applications'
    subprocess.run(create_applications_folder_command, check=True, shell=True)

    place_desktop_command = 'cp src/resources/desktop/postman.desktop ~/.local/share/applications/'
    subprocess.run(place_desktop_command, check=True, shell=True)