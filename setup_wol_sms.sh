#!/bin/bash

read -p "Are you ready to continue, and do you have the full path to 
your config.ini file, telephone number and mac address of the device 
to be woken up ready? [y/N]: " ready
if [[ ! "$ready" =~ ^[Yy]$ ]]; then
    echo "Exiting setup. Please run this script again when you're ready."
    exit 1
fi

echo "Update"
sudo apt update

echo "Installing required packages..."
sudo apt install -y wakeonlan python3-serial

echo "Python:"
python --version

read -p "Do you want to install minicom (for serial debugging)? [y/N]: " minicom_choice
if [[ "$minicom_choice" =~ ^[Yy]$ ]]; then
    sudo apt-get install -y minicom
fi

echo "Please edit config.ini now (leave editor when done)."
sleep 2
nano config.ini

read -p "Enter full path to your config.ini [$default_path]: " config_path
config_path=${config_path:-$default_path}

echo "Updating smsWake.py with config path..."
sed -i "s|config.read('.*')|config.read('$config_path')|" smsWake.py

echo "Adding script to crontab..."
crontab -l 2>/dev/null > mycron || true
cron_line="@reboot python3 /home/pi/wol/wake-on-lan-sms-pi/smsWake.py"
grep -Fxq "$cron_line" mycron || echo "$cron_line" >> mycron
crontab mycron
rm mycron

echo "Setup complete! Rebooting in 5 seconds..."
sudo reboot