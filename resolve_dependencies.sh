#!/bin/bash

# Export the distribution as an environment variable (if not already set)
if [ -z "$DISTRIBUTION" ]; then
  DISTRO=$(lsb_release -si 2>/dev/null || cat /etc/os-release | grep '^ID=' | cut -d'=' -f2- | tr -d '"')
	export DISTRIBUTION=${DISTRO^}
fi

echo "Detected distribution $DISTRIBUTION"

read -p "This will install the following dependencies python, pip, python-env and libnotify. Do you want to continue? (yes/no): " answer

if [ "$answer" != "yes" ]; then
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

install

echo "Dependencies resolved"
