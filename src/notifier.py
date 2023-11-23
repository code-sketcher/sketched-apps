from termcolor import colored
import subprocess


class Notifier:
    def __init__(self):
        pass

    def print_success(self, message):
        print(colored(message, 'green', attrs=['bold']))

    def print_warning(self, message):
        print(colored(message, 'yellow', attrs=['bold']))

    def print_error(self, message):
        print(colored(message, 'red', attrs=['bold']))

    def print_info(self, message):
        print(colored(message, 'blue', attrs=['bold']))

    def success(self, message):
        self.print_success(message)
        self.__notify('Success', message)

    def warning(self, message):
        self.print_warning(message)
        self.__notify('Warning', message)

    def error(self, message):
        self.print_error(message)
        self.__notify('Error', message, '--urgency=critical')

    def __notify(self, title, message, urgency='--urgency=normal'):
        subprocess.run(['notify-send', urgency, title, message], check=True)
