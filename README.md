# pihole-status

Pihole-status is an add-on module for your Pi-hole that displays realtime status information on a tiny OLED screen with no external monitor needed.

The information is divided into two alternating screens:

### System information:
- **IP address**: Displays the current Pi-hole ip address or blank if none is available.
- **CPU utilization**: CPU load average.
- **Memory in use / Total memory**: Useful to ensure that no processes are consuming more memory than expected.
- **Disk space used / Total disk space**: Useful to ensure there are no logs growing unbounded.
- **CPU temperature**: Thermal throttling will kick in at about 180F so the CPU temp should be considerably lower.
- **System uptime**: Useful to help indicate long-term stability.

### Pi-hole information:
- Blocked percentage
- Blocked count
- Total number of queries
- Domains blocked

---

## Installation

Like the Pi-hole install process itself, one-step installation of pihole-status is available to get started quickly using the following command:

### `curl -sSL https://raw.githubusercontent.com/bkolin/pihole-status/master/setup.sh | bash`

### Alternative Install Methods

Alternative methods are available which allow for review and modification of the code before installation. Note that both methods will ultimately download the latest pihole-status script from the repo, so if you make local changes to pihole-status.py you should not re-run the setup script.

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
wget -O pihole-status-setup.sh https://raw.githubusercontent.com/bkolin/pihole-status/master/setup.sh
sudo bash pihole-status-setup.sh
```
---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
