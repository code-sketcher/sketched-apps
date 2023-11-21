from src.app_manager import AppManager
from src.vs_code import VSCode
from src.beekeeper_studio import BeekeeperStudio
from src.docker import Docker
from src.kubectl import Kubectl
from src.app_tracker import AppTracker
from src.onlyoffice import Onlyoffice
from src.app_list import AppList

if __name__ == "__main__":
  app_list = AppList()
  app_list.install_list()
  #app = AppManager()
  #app.install('curl')

  #code = VSCode()
  #code.install()

  #beekeeper = BeekeeperStudio()
  #beekeeper.install()

  #docker = Docker()
  #docker.install()

  #kubectl = Kubectl()
  #kubectl.install()

  #onlyoffice = Onlyoffice()
  #onlyoffice.install()

  #AppTracker.display_installed_apps()
  #AppTracker.display_already_installed_apps()
  #AppTracker.display_failed_apps()
