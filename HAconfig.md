# HA Server Config

- SSL configuration:
  - Addon: `File editor`
    - Place the certs from the secrets into `/ssl/fullchain.pem` / `/ssl/privkey.pem`
    - Restart System
    - Ctrl + F5 reload the page (new certificate -> del browser cache)

```yml
# -> this has been migrated out of the config.yaml to  "Settings > System > Network"
ssl_certificate_path: /ssl/fullchain.pem
ssl_key_path: /ssl/privkey.pem
```

- Additional file-sessings and OS access:
  - Addon: `Advanced SSH & Web Terminal`
