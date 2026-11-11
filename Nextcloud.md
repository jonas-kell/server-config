# Nextcloud

Notes about the kubernetes nextcloud installation and documentation of processes

## occ

[See here](https://github.com/nextcloud/helm/tree/main/charts/nextcloud#running-occ-commands) how to run occ commands directly.

```cmd
export NEXTCLOUD_POD=$(kubectl get pods -n nextcloud --no-headers -o custom-columns=":metadata.name" | grep '^nextcloud' | grep -v 'postgresql')

# general command
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ"

# collection
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ maintenance:mode --on"
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ maintenance:mode --off"

kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ upgrade"
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ maintenance:repair"
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ maintenance:repair --include-expensive"
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ files:scan --all"

kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ db:add-missing-columns"
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ db:add-missing-indices"
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ db:add-missing-primary-keys"

kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php cron.php"
```

## Logs

If pod crashes, get some details out of the status page (can not be reached otherwise, because the kubernetes pod is not `ready`).

```cmd
kubectl exec -it -n nextcloud <pod> -c nextcloud-nginx -- curl -v -i localhost/status.php
```

Get the detailed logs

## Bruteforce protection

Query the amount of connections

```cmd
kubectl exec -it -n nextcloud nextcloud-postgresql-0 -- env PGPASSWORD="$(ansible-vault view secrets/nextcloud.yml | grep postgres_admin_pw | grep -oP '"\K[^"]+(?=")')" psql -U postgres

>>>

\c nextcloud

SELECT ip, COUNT(*) AS attempts FROM oc_bruteforce_attempts GROUP BY ip ORDER BY attempts DESC;

exit
```

Reset the counter:

```cmd
# NEXTCLOUD_POD from above

kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ security:bruteforce:attempts 10.42.0.1"
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ security:bruteforce:reset 10.42.0.1"
```

## Backups

[TODO](https://github.com/nextcloud/helm/tree/main/charts/nextcloud#backups)

Manually dump the database

```cmd
kubectl exec -it -n nextcloud nextcloud-postgresql-0 -- env PGPASSWORD="$(ansible-vault view secrets/nextcloud.yml | grep postgres_admin_pw | grep -oP '"\K[^"]+(?=")')" pg_dump -U postgres nextcloud > db.bak
```

Restore the database into postgresql

```cmd
# copy the database to the pod
kubectl cp ./nextcloud-sqlbkp_20260211.bak -n nextcloud nextcloud-postgresql-0:/tmp/nextcloud-sqlbkp.bak

# load
kubectl exec -it -n nextcloud nextcloud-postgresql-0 -- env PGPASSWORD="$(ansible-vault view secrets/nextcloud.yml | grep postgres_admin_pw | grep -oP '"\K[^"]+(?=")')" psql -U postgres -d template1 -c "DROP DATABASE \"nextcloud\";"
kubectl exec -it -n nextcloud nextcloud-postgresql-0 -- env PGPASSWORD="$(ansible-vault view secrets/nextcloud.yml | grep postgres_admin_pw | grep -oP '"\K[^"]+(?=")')" psql -U postgres -d template1 -c "CREATE DATABASE \"nextcloud\";"
kubectl exec -it -n nextcloud nextcloud-postgresql-0 -- env PGPASSWORD="$(ansible-vault view secrets/nextcloud.yml | grep postgres_admin_pw | grep -oP '"\K[^"]+(?=")')" psql -U postgres -d nextcloud -c "GRANT ALL PRIVILEGES ON SCHEMA public TO nextcloud;"
kubectl exec -it -n nextcloud nextcloud-postgresql-0 -- env PGPASSWORD="$(ansible-vault view secrets/nextcloud.yml | grep postgres_admin_pw | grep -oP '"\K[^"]+(?=")')" psql -U postgres -d nextcloud -f /tmp/nextcloud-sqlbkp.bak
```

## Updates and custom docker images

Only way to add smb support to the kubernetes nextcloud is seemingly to extend the image.

Updating will happen, when the image is updated...

For how to do this, see [this documentation](./docker/Readme.md)

## Things to do on a new Installation

- Insert the `Password Salt` and `Secret` in the config.php (needs to correspond to the database)
- Execute `occ maintenance:repair` to clear the frontend js caches
- Add `'default_phone_region' => 'DE',` into config
- Add `'maintenance_window_start' => 1,` into config
- Apps
  - Install external Apps
    - Tasks
    - Spreed (= Talk)
    - Polls
    - Notiy Push (= Client Push)
    - Forms
    - Epubviewer
    - Checksum
    - Calendar
  - Enable the app `External storage support`
  - Disable the app `AppAPI` ([see](https://apps.nextcloud.com/apps/app_api))
    - TODO maybe in the future fix it so that it can be used

## Bugs

Combination of Ubuntu 26.04 and k3s Postgresql: [Issue](https://github.com/containerd/containerd/pull/14487#issuecomment-6546999621)

```cmd
│ 2026-11-11 13:58:27.038 GMT [138] FATAL:  the database system is starting up                                                                                     │
│ 2026-11-11 13:58:28.688 GMT [145] FATAL:  the database system is starting up                                                                                     │
│ 2026-11-11 13:58:37.041 GMT [152] FATAL:  the database system is starting up                                                                                     │
│ 2026-11-11 13:58:38.693 GMT [159] FATAL:  the database system is starting up                                                                                     │
│ 2026-11-11 13:58:39.286 GMT [95] FATAL:  could not signal for checkpoint: Permission denied                                                                      │
│ 2026-11-11 13:58:39.293 GMT [1] LOG:  startup process (PID 95) exited with exit code 1                                                                           │
│ 2026-11-11 13:58:39.293 GMT [1] LOG:  aborting startup due to startup process failure                                                                            │
│ 2026-11-11 13:58:39.295 GMT [1] LOG:  database system is shut down
```

Temporary Solution:

```cmd
sysctl kernel.apparmor_restrict_unprivileged_unconfined
# gives:     kernel.apparmor_restrict_unprivileged_unconfined = 1

# Temporarily deactivate this (non-restart-permanent):
sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=0

# Reset the behavior:
sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=1
```
