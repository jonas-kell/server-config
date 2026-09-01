# TODO: not set up after cosmic transition

- mounts / favourites in file manager
- store the config toml files repeatable
- get Wifiman working

https://github.com/cosmic-utils

<!--  -->

flatpak install flathub io.github.cosmic_utils.camera
sudo apt-get install cosmic-store

<!-- install minimon from the cosmic store (CPU / etc. performance) -->

activate in applets -> configure to thigs you want to be displayed

<!--  -->

cargo install --git https://github.com/estin/cos-cli
cos-cli info

nano ~/.config/cosmic/com.system76.CosmicSettings.WindowRules/v1/tiling_exception_custom

```cmd
[
    (appid: "", title: ".*CopyQ.*", enabled: true),
]
```

<!--  -->

Clear gnome online accounts links -> non working cloud integrations

rm -rf ~/.config/goa-1.0

Google drive rclone shortcut just keeps working and can be reused (Applications->right-click->pin)

<!--  -->

sudo apt-get remove gnome-system-monitor
sudo apt-get install cosmic-monitor

<!--  -->

Show battery percentage!

touch ~/.config/cosmic/com.system76.CosmicAppletBattery/v1/show_percentage
echo true > ~/.config/cosmic/com.system76.CosmicAppletBattery/v1/show_percentage

<!--  -->

Auto rotate screen

sudo apt install iio-sensor-proxy wlr-randr

https://github.com/armaaar/cosmic-applet-rotation/releases/tag/v0.1.0

sudo dpkg -i cosmic-applet-rotation_0.1.0_amd64.deb

<!--  -->

Eduroam permanence

Install "geteduroam" from flatpak. Connect to eduroam WIFI

Get the uuid of the connection:

nmcli -f NAME,UUID,FILENAME connection

(netplan-NM-6e9f8193-5b84-4f60-ac87-26fcdafd0bb7-eduroam.nmconnection) in my case

sudo netplan get

-> gets more details (outputs a long list that should contain something like)

```cmd
.....
    NM-6e9f8193-5b84-4f60-ac87-26fcdafd0bb7:
      renderer: NetworkManager
      match: {}
      dhcp4: true
      dhcp6: true
      access-points:
        "eduroam":
          auth:
            key-management: "eap"
            method: "peap"
            anonymous-identity: "eduroam25@uni-saarland.de"
            identity: "redacted@uni-saarland.de"
            phase2-auth: "mschapv2"
            password: "redacted"
          networkmanager:
            uuid: "6e9f8193-5b84-4f60-ac87-26fcdafd0bb7"
            name: "eduroam (from geteduroam)"
            passthrough:
              connection.autoconnect-priority: "1"
              connection.permissions: "user:jonas:;"
              wifi-security.group: "ccmp;"
              wifi-security.pairwise: "ccmp;"
              wifi-security.proto: "rsn;"
              802-1x.altsubject-matches: "DNS:horus.net.uni-saarland.de;"
              802-1x.ca-path: "/home/jonas/.var/app/app.eduroam.geteduroam/data/geteduroam/ca"
              ipv6.addr-gen-mode: "default"
              ipv6.ip6-privacy: "-1"
              proxy._: ""
      networkmanager:
        uuid: "6e9f8193-5b84-4f60-ac87-26fcdafd0bb7"
        name: "eduroam (from geteduroam)"
......
```

get name of wifi adapter: (here wlp0s20f3)

```cmd
$ nmcli device status
DEVICE             TYPE      STATE                   CONNECTION
enx00e04c3608fa    ethernet  connected               Wired connection 5
docker0            bridge    connected (externally)  docker0
lo                 loopback  connected (externally)  lo
wlp0s20f3          wifi      disconnected            --
p2p-dev-wlp0s20f3  wifi-p2p  disconnected            --
vethab2f933        ethernet  unmanaged               --
```

nmcli connection delete "6e9f8193-5b84-4f60-ac87-26fcdafd0bb7" -> depending of the uuid of the generated eduroam connection

sudo nano /etc/netplan/01-eduroam.yaml

```cmd
network:
  version: 2
  renderer: NetworkManager
  wifis:
    wlp0s20f3:
      dhcp4: true
      dhcp6: true
      access-points:
        "eduroam":
          auth:
            key-management: eap
            method: peap
            anonymous-identity: "eduroam25@uni-saarland.de"
            identity: "redcted@uni-saarland.de"
            phase2-auth: mschapv2
            password: "DEIN_PASSWORT_HIER"
          networkmanager:
            passthrough:
              802-1x.altsubject-matches: "DNS:horus.net.uni-saarland.de;"
              802-1x.ca-path: "/etc/netplan/eduroam-ca"
              connection.autoconnect-priority: "1"
              wifi-security.group: "ccmp;"
              wifi-security.pairwise: "ccmp;"
              wifi-security.proto: "rsn;"
```

```cmd
sudo cp -r /home/jonas/.var/app/app.eduroam.geteduroam/data/geteduroam/ca /etc/netplan/eduroam-ca
sudo chmod 755 /etc/netplan/eduroam-ca
sudo chmod 644 /etc/netplan/eduroam-ca/*

sudo chmod 400 /etc/netplan/01-eduroam.yaml
sudo netplan apply
```
