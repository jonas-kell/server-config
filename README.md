# Server config

Management scripts for my personal servers and kubernetes setup.

[First time setup commands](FirstTimeCommands.md) (Most relevant for custom local installations, Like the piserver)

[HOW to set secrets](secrets/HOWTO.md)

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
    - `https://haserver.kellehorreur.de:8123`
    - `https://ha.kellehorreur.de:8123`
  - My Clound EX2 Ultra
    - 4TB HDD
    - `http://storageserver.kellehorreur.de`

## Local installation

```cmd
pip3 install ansible
pip3 install ansible-lint
pip3 install httpx urllib3 # unifi api dependencies
pip3 install jmespath # necessary for use of json_filter
pip3 install dnspython # necessary for use of dig module
pip3 install aiohttp asyncio # necessary for ionos api interaction

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
