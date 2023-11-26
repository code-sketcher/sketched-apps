# sketched-apps

A script that will install my applications on a clean system.
Already installed apps are skipped. 

Works for Ubuntu, Debian. 
## How to run

Clone this git repository and then run the following command:

```bash
$ make run
```

This will install all the apps found in `src/app_list.py` and some dependencies. 

Scrip is using snap for some apps (spotify, notesnook, discord). 
If you want those apps, you should install snap before running the scrip.

### Install snap
```bash
## Debian
$ sudo apt update && sudo apt install -y snap
```

## Good to know

### Ubuntu
On ubuntu maybe you want to install ubuntu-restricted-extras manually for codecs.

### Ulauncher
> #### Extensions
>>- SSH Launcher - https://github.com/jyvern/ulauncher-ssh
>>- Jetbrains launcher - https://github.com/brpaz/ulauncher-jetbrains
    - Add your project path like: ~/.config/JetBrains/PhpStorm2022.2/options/recentProjects.xml
>>- Network Manager - https://github.com/melianmiko/ulauncher-nmcli
