#!/bin/bash

# Export the distribution as an environment variable (if not already set)
if [ -z "$DISTRIBUTION" ]; then
  DISTRO=$(lsb_release -si 2>/dev/null || cat /etc/os-release | grep '^ID=' | cut -d'=' -f2- | tr -d '"')
	export DISTRIBUTION=${DISTRO^}
fi

echo "Detected distribution $DISTRIBUTION"

# Function to check if a command is available
command_exists() {
  command -v "$1" >/dev/null 2>&1
}



# Function to install Python and pip based on the Linux distribution
install() {
  case $DISTRIBUTION in
    Debian|Ubuntu)
      sudo apt update
      sudo apt install -y python3-full python3-venv python3-pip libnotify-bin
      ;;

    Arch)
      sudo pacman -Syu --noconfirm python python-pip libnotify
      ;;

    Fedora)
      sudo dnf install -y python3-full python3-venv python3-pip libnotify
      ;;

    *)
      echo "Unsupported distribution: $distribution"
      exit 1
      ;;
  esac
}

# Check if Python is installed
if ! command_exists python3; then
  # Install Python and pip
  install

  # Check if installation was successful
  if ! command_exists python3; then
    echo "Failed to install Python."
    exit 1
  fi
fi

# Check if pip is installed
if ! command_exists pip3; then
  echo "Installing pip..."
  sudo apt install -y python3-pip
fi

# Check if can send-notify
if ! command_exists notify-send; then
  echo "Installing libnotify"
	install
fi

echo "Python, venv and pip are installed and ready to use on ditribution: $DISTRIBUTION"
