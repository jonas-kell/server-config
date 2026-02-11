# HA Server Config

- SSL configuration:
  - Addon: `File editor`
    - Place the certs from the secrets into `/ssl/fullchain.pem` / `/ssl/privkey.pem`
    - Restart System
    - Ctrl + F5 reload the page (new certificate -> del browser cache)

```yml
#! /homeassistant/configuration.yaml

# ssl
http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
```

- Additional file-sessings and OS access:
  - Addon: `Advanced SSH & Web Terminal`
