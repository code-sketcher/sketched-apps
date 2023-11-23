#!/bin/bash

BLUE='\033[34m'
CYAN='\033[36m'
RESET='\033[0m'

# Export the distribution as an environment variable (if not already set)
if [ -z "$DISTRIBUTION" ]; then
  DISTRO=$(lsb_release -si 2>/dev/null || cat /etc/os-release | grep '^ID=' | cut -d'=' -f2- | tr -d '"')
	export DISTRIBUTION=${DISTRO^}
fi

echo -e "${CYAN}Detected distribution $DISTRIBUTION ${RESET}"

read -p "$(echo -e "${BLUE}This will install the following dependencies python, pip, python-env, and libnotify.${RESET}\nDo you want to continue? (y/n): ")" answer

if [ "$answer" != "y" ]; then
    echo "Script terminated. Goodbye!"
    exit 1
fi

echo "Great! Let's install some apps..."
sleep 3

install() {
  case $DISTRIBUTION in
    Debian|Ubuntu)
      sudo apt update
      sudo apt install -y python3 python3-venv python3-pip libnotify-bin
      ;;

    Arch)
      sudo pacman -Syu --noconfirm python python-pip libnotify
      ;;

    Fedora)
      sudo dnf install -y python3 python3-venv python3-pip libnotify
      ;;

    *)
      echo "Unsupported distribution: $distribution"
      exit 1
      ;;
  esac
}

config() {
  case $DISTRIBUTION in
    Debian)
      echo "PATH="/home/$USER/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"" | sudo tee /etc/environment
      source /etc/environment
      ;;
  esac
}

install
config

echo -e "${CYAN}Dependencies resolved${RESET}"
