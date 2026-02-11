# Hoto setup secrets, where to find them

## SSL

(From Ionos)

- Generate Certificate
  - Thereby a private key file is being downloaded
    - ssl_certificate_key -> privkey.pem;
- Wait for it to be issued
  - Now Download the Certificate and the Intermediate
  - Append FIRST Certificate and THEN Intermediate into
    - ssl_certificate -> fullchain.pem;

## Ubiquiti API token

- Like described in `/roles/unifi_firewall_writing/meta/argument_specs.yml`
  - Generate: https://unifi.ui.com/ > Network > Settings > Control Plane > Integrations

```yml
ubiquiti_api_token: "..."
```

## Ionos DNS API

- Like described in `/collections/ansible_collections/custom/dns/plugins/modules/ionosdns.py`
  - https://developer.hosting.ionos.de/keys

```yml
ionos_api_prefix: "..."
ionos_api_key: "..."
```
