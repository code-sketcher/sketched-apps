from termcolor import colored
from plyer import notification
import subprocess

class Notifier:
  def __init__(self):
    pass

  def success(self, message):
    print(colored(message, 'green'))
    self.__notify('Success', message)

  def error(self, message):
    print(colored(message, 'red'))
    self.__notify('Error', message)

  def __notify(self, title, message):
    subprocess.run(['notify-send', title, message], check=True)
