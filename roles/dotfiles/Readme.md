# Dotfiles and System maintenance commands

## Git push without GitLab CI

```cmd
git push -o ci.skip
```

## Upgrade (safe)

```cmd
sudo apt-get --with-new-pkgs upgrade
```

## Kubernetes commands (useful)

Get pods

```cmd
kubectl get pods -n mathezirkel-app
```

Set and delete ENV variables on running installations

```cmd
kubectl set env -n mathezirkel-app deployment/mathezirkel-app-backend-webserver RUST_LOG-

kubectl set env -n mathezirkel-app deployment.apps/mathezirkel-app-backend-webserver RUST_LOG=debug,actix=off,diesel_migrations=off,hyper=off
```

Interactive shell

```cmd
kubectl exec -n mathezirkel-app -it mathezirkel-app-backend-webserver-...... -- /bin/bash
```
