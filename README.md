# Pihole-status

Pihole-status is an add-on module for your Pi-hole that displays realtime status information on a tiny OLED screen with no external monitor needed. Note that if you have a small LCD screen attached, the Pi-hole software itself already includes a [great solution](https://docs.pi-hole.net/core/pihole-command/#chronometer) to displaying realtime status.

The information is divided into two alternating screens:

### System information:
- **IP address**: Displays the current Pi-hole ip address or blank if none is available.
- **CPU utilization**: CPU load average.
- **Memory in use / Total memory**: Useful to ensure that no processes are consuming more memory than expected.
- **Disk space used / Total disk space**: Useful to ensure there are no logs growing unbounded.
- **CPU temperature**: Thermal throttling will kick in at about 180F so the CPU temp should be considerably lower.
- **System uptime**: Useful to help indicate long-term stability.

### Pi-hole information:
- **Pi-hole version**: The core pi-hole software version
- **Blocked percentage**: The percentage of ads blocked today
- **Blocked count**: The total count of ads blocked today
- **Total number of queries**: The number of DNS queries fielded today
- **Domains blocked**: The number of domains blocked, summed across loaded blocklists
- **Pi-hole update available**: If the available version of the core pi-hole version does not match the current version, this field displays "Yes", otherwise it displays "No"

---

## Installation

Like the Pi-hole install process itself, one-step installation of pihole-status is available to get started quickly using the following command:

### `curl -sSL https://raw.githubusercontent.com/bkolin/pihole-status/master/setup.sh | bash`

### Alternative Install Methods

Alternative methods are available which allow for review and modification of the code before installation. Note that both methods will ultimately download the latest pihole-status.py script from the repo, so if you make local changes to pihole-status.py you should not re-run the setup script.

### Method 1: Clone the git repository and run

```bash
cd
mkdir pihole-status-install
git clone https://github.com/bkolin/pihole-status pihole-status-install
cd pihole-status-install
sudo bash setup.sh
```

### Method 2: Manually download the installer and run

```bash
wget -O setup.sh https://raw.githubusercontent.com/bkolin/pihole-status/master/setup.sh
sudo bash setup.sh
rm setup.sh
```
---

## Hardware
Virtually any modern SSD1306-based 128x64 OLED screen will work. Some manufacturers make raspi-focused hardware that requires no additional hardware, but with a little work almost all of them can be connected. If possible try for one that presses directly onto the pin headers and looks approximately like this:



## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
