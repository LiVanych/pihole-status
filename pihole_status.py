#!/usr/bin/python3
#
#
# pihole-status
#   https://github.com/bkolin/pihole-status
#
# This script shows various status data about the connected pi-hole on
# an attached 13-6-based OLED screen:
#
# - IP address
# - Blocked percentage
# - Total blocked count / Total number of queries
# - CPU utilization
# - CPU temp
# - Memory in use / Total memory
# - Disk space used / Total disk space
#
# Based on the Adafruit 1306 example at:
#   https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage 
#
# Pi-hole stats extraction based on Matt Hawkins' implementation at: 
#   https://bitbucket.org/MattHawkinsUK/rpispy-misc/src/master/pihole/
#
# This implementation is not interactive - no LEDs or switches are used.
#


# Standard libraries
import time
import math
import json
import requests
import subprocess

# Graphics libraries
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Adafruit library for I2C OLED screen
import Adafruit_SSD1306

# Screen refresh frequency:
refresh = 30

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=2)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load Truetype font from https://www.dafont.com/bitmap.php
# VCR OSD Mono by Riciery Leal
font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf',15)
font2 = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf',40)

#font = ImageFont.load_default()

def clear_screen():
  # Draw a black filled box to clear the image.
  draw.rectangle((0,0,width,height), outline=0, fill=0)

clear_screen()

# Show Start Script text
draw.text((x, top), "Start Script",  font=font, fill=255)
disp.image(image)
disp.display()

# Default mode, show large percentage
mode=0
counter=1

while True:

  if counter > refresh:
    counter = 0
    clear_screen()

    if mode == 0:
      # Pi-hole data

      # Get Pi-Hole data from local admin web page
      r = requests.get("http://localhost/admin/api.php?summary")

      # Display large Pi-Hole ads blocked percentage
      draw.text((x, top-2), "%s%%" % r.json()["ads_percentage_today"],  font=font2, fill=255)
      draw.text((x, top+32), "Ads blocked: %s" % r.json()["ads_blocked_today"], font=font, fill=255)   
      draw.text((x, top+48), "DNS queries: %s" % r.json()["dns_queries_today"], font=font, fill=255)
 
      # Toggle
      mode = 1

    elif mode == 1:
      # System data

      # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
      cmd = "hostname -I | cut -d\' \' -f1"
      IP = subprocess.check_output(cmd, shell = True).decode('UTF-8')

      cmd = "top -bn1 | grep load | awk '{printf \"C: %.2f\", $(NF-2)}'"
      CPU = subprocess.check_output(cmd, shell = True).decode('UTF-8')
      
      cmd = "free -m | awk 'NR==2{printf \"M: %s/%sMB\", $3,$2 }'"
      MemUsage = subprocess.check_output(cmd, shell = True).decode('UTF-8')
      
      cmd = "df -h | awk '$NF==\"/\"{printf \"D: %d/%dGB\", $3,$2}'"
      Disk = subprocess.check_output(cmd, shell = True).decode('UTF-8')

      cmd = "vcgencmd measure_temp"
      Temp = subprocess.check_output(cmd, shell = True).decode('UTF-8')
      Temp = Temp.replace("temp=","")
      # Display in F
      Temp = (Temp * 9/5) + 32

      # Display system stats
      draw.text((x, top), "IP: " + IP),  font=font, fill=255)    
      draw.text((x, top+16), "CPU:  " + CPU, font=font, fill=255)
      draw.text((x, top+32), "Mem:  " + MemUsage, font=font, fill=255)
      draw.text((x, top+40), "Disk: " + Disk,font=font, fill=255)
      draw.text((x, top+48), "Temp: " + Temp,font=font, fill=255)

      mode=0
    
    # Display image.
    disp.image(image)
    disp.display()

  counter += 1
  time.sleep(1)
