# Server config

Management scripts for my personal servers and kubernetes setup.

[First time setup commands](FirstTimeCommands.md) (Most relevant for custom local installations, Like the piserver)

[HOW to set secrets](secrets/HOWTO.md)

This is also my automatically deployed dotfiles repository (see below)

[How to configure required things on Unifi](./Unifi.md)

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
  - Raspberry Pi 4B, 4GB
    - 64 GB SD card
    - [Home Assistant OS, with Home Assistant Core](HAconfig.md)
      - TODO symmetric http encryption for [the pico lock](https://github.com/jonas-kell/home-assistant-custom-components-pico-lock)
      - TODO LED matrix HA conversion [See](https://github.com/jonas-kell/led-matrix) (also with symmetric encryption)
    - `root@haserver.kellehorreur.de`
    - `https://haserver.kellehorreur.de:8123` - IPv4 internal
    - `https://ha.kellehorreur.de:8123` - IPv6 + external IPv4
  - My Clound EX2 Ultra
    - 4TB HDD
    - `http://storageserver.kellehorreur.de`
- Other DNS entries for services
  - `cloud.kellehorreur.de`
    - Personal Nextcloud installation to access the storageserver
    - See [Nextcloud](./Nextcloud.md)
    - [Test your installation](https://scan.nextcloud.com/)
  - `pihole.kellehorreur.de`
    - Only points to the local adress of piserver -> DNS just inside the LAN
    - See [Pihole](./Pihole.md)
  - `talk-backend.kellehorreur.de`
    - TURN server
    - TODO [High-performance backend for Nextcloud talk](https://nextcloud-talk.readthedocs.io/en/latest/quick-install/)
  - `mailbackup.kellehorreur.de`
    - TODO [Experiment-Notes](https://github.com/jonas-kell/mail-backup)
  - `mail.kellehorreur.de`
    - TODO maybe host onw mailserver. [Experiment-Notes](https://gist.github.com/jonas-kell/940e91d0483e89908b44f3f8ba2c85fa)
  - `vpn.kellehorreur.de`
    - TODO setup VPN (maybe with [udp-over-https](https://github.com/jonas-kell/udp-over-https))
  - `dev.kellehorreur.de`
    - Local development host. Used for [this project](https://github.com/jonas-kell/ssl-dev-termination/)
  - `keyboard-proxy.kellehorreur.de`
    - Proxy for [smartphone-keyboard-remote](https://github.com/jonas-kell/smartphone-keyboard-remote)
  - Other TODOs
    - TODO [batch-viewer-for-reddit proxy](https://github.com/jonas-kell/batch-viewer-for-reddit)
    - TODO [license key management](https://github.com/jonas-kell/jta-display-wall-adapter)

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
patch -N -d ./collections/ansible_collections/ubiquiti/unifi_api -p0 < ./collections/patches/fix-unifi-spec-url.patch || true
ansible-galaxy collection install -r collections/requirements.yml -p ./collections --force
ansible-galaxy install -r roles/requirements.yml --force
```

<!--
generate the patch

copy the file, add .orig to name
change the function

    def get_spec_url(self, version: str) -> str:
        application = self.get_name()
        spec_url = f"{OPENAPI_SPEC_BASE_URL}/{application}/v{version}/integration.json"

        # Check if the remote spec exists.
        try:
            with httpx.Client() as c:
                resp = c.head(spec_url)
                if resp.status_code == 200:
                    return spec_url
        except Exception:
            pass

        self.module.warn(f"Spec for version {version} not found, falling back to latest available version.")

        versions_endpoint = f"{DEV_PORTAL_BASE_URL}/v1/api-docs?application={application}"
        resp = self.rt.call(versions_endpoint)

        data = resp.json().get("data", [])

        if isinstance(data, dict):
            versions_data = data.get("versions", [])
        else:
            versions_data = data

        available_versions = [
            v.get("version").lstrip("v")
            for v in versions_data
            if isinstance(v, dict) and "version" in v
        ]

        # Find the closest version (<= requested version)
        closest_version = None
        for v in sorted(available_versions, reverse=True):
            if v <= version:
                closest_version = v
                break

        if not closest_version and available_versions:
            closest_version = available_versions[-1]

        version = closest_version

        return f"{OPENAPI_SPEC_BASE_URL}/{application}/v{version}/integration.json"

cd ./collections/ansible_collections/ubiquiti/unifi_api
diff -u plugins/module_utils/base_module.py.orig plugins/module_utils/base_module.py > ../../../patches/fix-unifi-spec-url.patch
-->

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

The files live in the [dotfiles role](./roles/dotfiles/).

```cmd
ansible-playbook playbooks/local.yml --ask-become-pass
```

(Configuration of `rclone` needed manually, see [role](./roles/dotfiles/tasks/drive.yml))
