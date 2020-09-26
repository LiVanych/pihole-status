#!/bin/sh

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
