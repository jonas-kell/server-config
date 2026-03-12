# Nextcloud

Notes about the kubernetes nextcloud installation and documentation of processes

## occ

[See here](https://github.com/nextcloud/helm/tree/main/charts/nextcloud#running-occ-commands) how to run occ commands directly.

```cmd
export NEXTCLOUD_POD=$(kubectl get pods -n nextcloud --no-headers -o custom-columns=":metadata.name" | grep '^nextcloud' | grep -v 'postgresql')

# general command
kubectl exec -n nextcloud $NEXTCLOUD_POD -- su -s /bin/sh www-data -c "php occ"
```

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
