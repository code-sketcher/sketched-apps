from src.app_manager import AppManager
from src.vs_code import VSCode
from src.beekeeper_studio import BeekeeperStudio
from src.docker import Docker
from src.kubectl import Kubectl


if __name__ == "__main__":
  app = AppManager()
  app.install('curl')

  code = VSCode()
  code.install()

  beekeeper = BeekeeperStudio()
  beekeeper.install()

  docker = Docker()
  docker.install()

  kubectl = Kubectl()
  kubectl.install()
