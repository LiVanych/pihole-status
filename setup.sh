#!/bin/sh

# -e means to exit if any command in this script has a non-zero exit status.
# This should help prevent broken installs.
set -e

cd ~
mkdir pihole-status
cd pihole-status

wget -O pihole_status.py https://raw.githubusercontent.com/bkolin/pihole-status/master/pihole_status.py

# Install dependencies:
sudo apt install -y python3-dev
sudo apt install -y python3-pip
sudo apt install -y python-smbus i2c-tools
sudo apt install -y python3-pil
sudo apt install -y python3-setuptools

# If gpio pins are going to be used:
# sudo apt install -y python3-rpi.gpio

# Install the Adafruit SSD1306 OLED driver:
sudo pip3 install adafruit-circuitpython-ssd1306

# Add a crontab entry to start the OLED updating script on boot:
# Note: On Debian-based systems the files in cron.d should not have an extension.
sudo bash -c 'echo "@reboot pi python3 /home/pi/pihole-status/pihole_status.py &" > /etc/cron.d/pihole_status'

echo "\nPihole-status installation complete."
echo '\nEnsure I2C is enabled via "sudo raspi-config ==> Interfacing Options ==> I2C", then reboot to activate OLED screen.'
