from notifier import Notifier

class AppTracker:
  installed_apps = set()
  already_installed_apps = set()

  @staticmethod
  def mark_installed(app_name):
    AppTracker.installed_apps.add(app_name)

  @staticmethod
  def mark_already_installed(app_name):
    AppTracker.already_installed_apps.add(app_name)

  @staticmethod
  def display_installed_apps():
    notify = Notify()
    notify.print_success(', '.join(installed_apps))

  @staticmethod
  def display_already_installed_apps():
    notify = Notify()
    notify.print_info(', '.join(already_installed_apps))

  @staticmethod
  def display_failed_apps():
    notify = Notify()
    notify.print_error(', '.join(failed_apps))
