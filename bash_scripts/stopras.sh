#!/bin/bash
# alias stopras = 'bash /home/pi/ras/bash_scripts/stopras.sh'
sudo systemctl stop watchdog
sudo systemctl stop ras-launcher