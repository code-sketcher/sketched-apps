from termcolor import colored
import subprocess


class Notifier:
  def __init__(self):
    pass

  def success(self, message):
    print(colored(message, 'green', attrs=['bold']))
    self.__notify('Success', message)

  def warning(self, message):
    print(colored(message, 'yellow', attrs=['bold']))
    self.__notify('Warning', message)

  def error(self, message):
    print(colored(message, 'red', attrs=['bold']))
    self.__notify('Error', message, '--urgency=critical')

  def print_info(self, message):
    print(colored(message, 'blue', attrs=['bold']))

  def __notify(self, title, message, urgency='--urgency=normal'):
    subprocess.run(['notify-send', urgency, title, message], check=True)
