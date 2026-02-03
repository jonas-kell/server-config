# Server config

Management scripts for my personal servers and kubernetes setup.

## What is deployed

- Ionos
  - [VPS 4 4 120](./Ionosconfig.md)
    - Ubuntu 24.04
    - `root@ionosserver.kellehorreur.de`
- Local
  - Raspberry Pi 4B, 8GB
    - 64 GB SD card
    - TODO choose os for kuberentes server
    - `pi@piserver.kellehorreur.de`
    - `https://cloud.kellehorreur.de`
  - Raspberry Pi 4B, 4GB
    - 64 GB SD card
    - Home Assistant OS, with Home Assistant Core
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
```

## Usage

```cmd
# Ping servers
ansible ionos -m ping
ansible local -m ping
# or
ansible all -m ping

# Install dependencies
ansible-galaxy collection install -r collections/requirements.yml -p ./collections
ansible-galaxy install -r roles/requirements.yml

# Run the deploying/configuring playbook
ansible-playbook playbooks/main.yml
```
