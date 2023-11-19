import subprocess
from src.notifier import Notifier

class AppManager:
  def __init__(self): 
    self.notify = Notifier()
  
  def install(self, app_name):
    try:
      subprocess.run(['sudo', 'nalas', 'install', '-y', app_name], check=True)
      self.notify.success(f"{app_name} has been installed  successfully.")
    except subprocess.CalledProcessError as e:
      self.notify.error(f"Failed to install {app_name}. Error: {e}")      
