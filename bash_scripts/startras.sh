#!/bin/bash
# alias startras = 'bash /home/pi/ras/bash_scripts/startras.sh'
sudo systemctl start watchdog
sudo systemctl start ras-launcher

echo "ras launched"