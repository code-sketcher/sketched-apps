from src.app_list import AppList
from src.distribution import Distribution

if __name__ == "__main__":
    distribution = Distribution()
    distribution.config()

    app_list = AppList()
    app_list.install()
    app_list.display_results()
