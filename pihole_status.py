#!/usr/bin/python3
#
#
# pihole-status
#   https://github.com/bkolin/pihole-status
#
# This script shows various status data about the connected pi-hole on
# an attached 13-6-based OLED screen:
#
# System information:
# - IP address
# - CPU utilization
# - Memory in use / Total memory
# - Disk space used / Total disk space
# - CPU temperature
# - System uptime
#
# Pi-hole information:
# - Pi-hole version
# - Blocked percentage
# - Blocked count
# - Total number of queries
# - Domains blocked
# - Pi-hole update available
#
# Based on the Adafruit 1306 example at:
#   https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage 
#
# Pi-hole stats extraction based Matt Hawkins' implementation at: 
#   https://bitbucket.org/MattHawkinsUK/rpispy-misc/src/master/pihole/
#

# Standard libraries
import time
import math
import json
import requests
import subprocess
from datetime import datetime

# Graphics libraries
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# I2C ibraries
from board import SCL, SDA
import busio

# Adafruit library for I2C OLED screen
import adafruit_ssd1306

# Screen refresh frequency:
refresh = 8 

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
 
# Create the SSD1306 OLED class
# The first two parameters are the pixel width and pixel height. Note that this
# script assumes 64 pixels of height and will need to be adjusted for other
# dimensions.
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
 
# Clear display
disp.fill(0)
disp.show()

# Create blank image for drawing
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Some constants to help with layout
padding = 0 
top = padding
bottom = height-padding
border = 5
# Move left to right keeping track of the current x position for drawing shapes
x = 0

font = ImageFont.load_default()

def clear_screen():
  # Draw a black filled box to clear the image.
  draw.rectangle((0,0,width,height), outline=0, fill=0)

def highlight_text(text, font):
  draw.rectangle((0,0,width,height), outline=255, fill=255)
  draw.rectangle((border, border, width - border - 1, height - border - 1),
      outline=0,
      fill=0,
  )
  (font_width, font_height) = font.getsize(text)
  draw.text((width/2 - font_width/2, height/2 - font_height/2) , text,  font=font, fill=255)

# Display startup text
title = "Pi-hole Status"
highlight_text(title, font)
disp.image(image)
disp.show()

# Default mode to showing system info first
mode = 0
counter = 1

while True:

  if counter > refresh:
    counter = 0
    clear_screen()

    if mode == 0:
      # Pi-hole data

      # Get Pi-Hole data from local admin web page
      try:
        r = requests.get("http://localhost/admin/api.php?summary")

        # We will retrieve both the current version and the latest version
        # to see if an update is available.

        # Note: 'pihole' -v -p -[c|l] to get the current and latest version of the pihole core
        # unfortunately has a number of different outputs depending on what information is available
        # locally. Sometimes the output starts with "Current" and sometimes it does not. We will
        # reverse the words so we can grab the version from the end of the sentence easily at
        # the beginning, and then chop off the period or ) if it exists.
        # Example output:
        #   Current Pi-hole version is v5.1.2.
        #   Pi-hole version is v5.1.2 (Latest: v5.1.2)


        cmd = "/usr/local/bin/pihole -v -p -c | awk \'{for (i=NF;i>0;i--){printf $i\" \"}}\' | cut -d\' \' -f1 | sed \'s/\.$//\' | sed \'s/)$//\'"
        Version = subprocess.check_output(cmd, shell = True).decode('UTF-8')
        #now = datetime.now()

        cmd = "/usr/local/bin/pihole -v -p -l | awk \'{for (i=NF;i>0;i--){printf $i\" \"}}\' | cut -d\' \' -f1 | sed \'s/\.$//\' | sed \'s/)$//\'"
        LatestVersion = subprocess.check_output(cmd, shell = True).decode('UTF-8')

        UpdateAvailable = "No"
        if LatestVersion.startswith('v') and Version != LatestVersion:
          UpdateAvailable = "Yes"

        # Display Pi-hole stats
        draw.text((x, top), "Pi-hole: " + Version,  font=font, fill=255)
        draw.text((x, top+12), "Block %%: %s%%" % r.json()["ads_percentage_today"],  font=font, fill=255)
        draw.text((x, top+22), "Ads blocked: %s" % r.json()["ads_blocked_today"], font=font, fill=255)
        draw.text((x, top+32), "DNS queries: %s" % r.json()["dns_queries_today"], font=font, fill=255)
        draw.text((x, top+42), "Domains: %s" % r.json()["domains_being_blocked"], font=font, fill=255)
        draw.text((x, top+52), "Update available: " + UpdateAvailable, font=font, fill=255)

      except requests.exceptions.RequestException as e:  # This is the correct syntax
        # We choose to keep running to see if the pi-hole web interface comes up rather than raise SystemExit(e)
        highlight_text("Pi-hole is DOWN!!!", font)
        
      # Toggle
      mode = 1

    elif mode == 1:
      # System data

      # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load

      # Note: subprocess.check_output returns the process output with a trailing \n. Use strip() to remove it.

      cmd = "hostname -I | cut -d\' \' -f1"
      IP = subprocess.check_output(cmd, shell = True).decode('UTF-8')

      cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
      CPU = subprocess.check_output(cmd, shell = True).decode('UTF-8').strip()
      
      cmd = "free -m | awk 'NR==2{printf \"%s / %sMB\", $3,$2 }'"
      MemUsage = subprocess.check_output(cmd, shell = True).decode('UTF-8').strip()
      
      cmd = "df -h | awk '$NF==\"/\"{printf \"%d / %dGB\", $3,$2}'"
      Disk = subprocess.check_output(cmd, shell = True).decode('UTF-8').strip()

      # We just want the numerical portion of the temperature:
      cmd = "vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'"
      Temp = subprocess.check_output(cmd, shell = True).decode('UTF-8').strip()
      # Round to nearest degree, display in F
      Temp_float = round((float(Temp)) * 9/5 + 32, 1) 
      Temp = str(Temp_float)

      cmd = "uptime -p | cut -d\' \' -f2,3,4,5,6,7,8,9"
      Uptime = subprocess.check_output(cmd, shell = True).decode('UTF-8').strip()

      # Display system stats
      draw.text((x, top), "IP: " + IP,  font=font, fill=255)    
      draw.text((x, top+12), "CPU:  " + CPU, font=font, fill=255)
      draw.text((x, top+22), "Mem:  " + MemUsage, font=font, fill=255)
      draw.text((x, top+32), "Disk: " + Disk,font=font, fill=255)
      draw.text((x, top+42), "Temp: " + Temp + "F",font=font, fill=255)
      draw.text((x, top+52), "Up: " + Uptime,font=font, fill=255)

      mode=0
    
    # Display image
    disp.image(image)
    disp.show()

  counter += 1
  time.sleep(1)
