# Server config

Management scripts for my personal servers and kubernetes setup.

[First time setup commands](FirstTimeCommands.md) (Most relevant for custom local installations, Like the piserver)

[HOW to set secrets](secrets/HOWTO.md)

This is also my automatically deployed dotfiles repository (see below)

## What is deployed

- Ionos
  - [VPS 4 4 120](./Ionosconfig.md)
    - Ubuntu 24.04
    - `root@ionosserver.kellehorreur.de`
- Local
  - Raspberry Pi 4B, 8GB
    - 64 GB SD card
    - Ubuntu 24.04
    - `pi@piserver.kellehorreur.de`
    - `https://cloud.kellehorreur.de`
  - Raspberry Pi 4B, 4GB
    - 64 GB SD card
    - [Home Assistant OS, with Home Assistant Core](HAconfig.md)
    - `root@haserver.kellehorreur.de`
    - `https://haserver.kellehorreur.de:8123` - IPv4 internal
    - `https://ha.kellehorreur.de:8123` - IPv6 + external IPv4
  - My Clound EX2 Ultra
    - 4TB HDD
    - `http://storageserver.kellehorreur.de`
- Other DNS entries for services
  - `pihole.kellehorreur.de`
    - Only points to the local adress of piserver -> DNS just inside the LAN
  - `mailbackup.kellehorreur.de`
  - `mail.kellehorreur.de`
  - `vpn.kellehorreur.de`
  - `dev.kellehorreur.de`

## Local installation

Must be ran to install this in a working manner locally (is not in the automatic install for `local.yml`, as you need ansible working for this to be executed, so that is not helpful...)

```cmd
pip3.12 install pipx

pipx install --include-deps ansible --force
pipx install ansible-lint --force

pipx inject ansible netaddr # ipv6 filter
pipx inject ansible httpx urllib3 # unifi api dependencies
pipx inject ansible jmespath # necessary for use of json_filter
pipx inject ansible dnspython # necessary for use of dig module
pipx inject ansible aiohttp asyncio # necessary for ionos api interaction

# Install dependencies
curl -L -o ./collections/downloads/ubiquiti-unifi_api-latest.tar.gz https://apidoc-cdn.ui.com/ansible-module/ubiquiti-unifi_api-latest.tar.gz
ansible-galaxy collection install ./collections/downloads/ubiquiti-unifi_api-latest.tar.gz -p ./collections --force
ansible-galaxy collection install -r collections/requirements.yml -p ./collections --force
ansible-galaxy install -r roles/requirements.yml --force
```

## Usage

```cmd
# Ping servers
ansible ionos -m ping
ansible local -m ping
# or
ansible all -m ping
```

Run the deploying/configuring playbook

```cmd
ansible-playbook playbooks/main.yml
```

Update remote servers

```cmd
ansible-playbook playbooks/upgrade.yml
```

Set ipv6-firewalls on unifi devices and ionos DNS

```cmd
ansible-playbook playbooks/unifi_ipv6_firewall_config.yml
```

## Dotfiles

Install a local Linux System (tested on and designed for Pop-Os at the moment).
This Repository doubles as my personal dotfiles repository.

The files live in the [dotfiels role](./roles/dotfiles/).

```cmd
ansible-playbook playbooks/local.yml --ask-become-pass
```

(Configuration of `rclone` needed manually, see [role](./roles/dotfiles/tasks/drive.yml))
