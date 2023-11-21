from src.notifier import Notifier
import sys
import subprocess

class Distribution:
  def __init__(self):
    self.notify = Notifier()

  def get_name(self):
    try:
      with open('/etc/os-release', 'r') as os_release:
        for line in os_release:
          if line.startswith('ID='):
            distro_id = line.split('=')[1].strip().strip('"')
            return distro_id.capitalize()
    except FileNotFoundError:
      self.notify.error(f"Failed to determine distribution!")
      sys.exit(1)      

  def config(self):
    if self.get_name() == 'Debian':
      subprocess.run('sudo apt-add-repository --component contrib', check=True, shell=True)
      subprocess.run('sudo apt-add-repository --component non-free', check=True, shell=True)

