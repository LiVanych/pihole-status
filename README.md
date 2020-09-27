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

In the spirit of the Pi-hole itself, one-step installation is available to get started quickly using the following command:

### `curl -sSL https://raw.githubusercontent.com/bkolin/pihole-status/master/setup.sh | bash`
- Do this

### Alternative Install Methods

Also in the spirit of the Pi-hole installation, there are alternative installation methods available which allow for review and modification of the code before installation:

### Method 1: Clone the git repository and run

```bash
git clone https://github.com/bkolin/pihole-status pihole-status-install
cd "pihole-status-install"
sudo bash setup.sh
```

### Method 2: Manually download the installer and run

```bash
wget -O basic-install.sh https://install.pi-hole.net
sudo bash basic-install.sh
```

```shell
$ somecommand
$ some other command
```

### Step 1
- Do this

### Step 2
- Then this

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
