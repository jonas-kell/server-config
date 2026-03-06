# Hoto setup secrets, where to find them

## SSL

Like described in the [SSL config](./../SSL.md)

## Ubiquiti API token

- Like described in `/roles/unifi_firewall_writing/meta/argument_specs.yml`
  - Generate: [https://unifi.ui.com/](https://unifi.ui.com/) > Network > Settings > Control Plane > Integrations

```yml
ubiquiti_api_token: "..."
```

## Ionos DNS API

- Like described in `/collections/ansible_collections/custom/dns/plugins/modules/ionosdns.py`
  - [https://developer.hosting.ionos.de/keys](https://developer.hosting.ionos.de/keys)

```yml
ionos_api_prefix: "..."
ionos_api_key: "..."
```

## K3s

Taken from [the sample inventory](https://github.com/k3s-io/k3s-ansible/blob/main/inventory-sample.yml):

The token should be a random string of reasonable length. You can generate one with the following commands:

```cmd
openssl rand -base64 64

# create the symlink (not needed in the future typically)
ln -s ../../secrets/k3s_token.yml inventories/group_vars/k3s_cluster.yml
```

You can use ansible-vault to encrypt this value / keep it secret.

## Kubeconfigs

Set the Kubeconfigs like described [in this cheat sheet](./../helm/Kubectl.md)

## Deploy

```cmd
ssh-keygen -t ed25519 \
  -C "flux-deploy-key" \
  -f secrets/flux_deploy_key

ansible-vault encrypt secrets/flux_deploy_key
ansible-vault encrypt secrets/flux_deploy_key.pub
```

Put the public key as a deploy key for this repo (WITH write access)

## Pihole

```cmd
ansible-vault edit secrets/pihole.yml
```

```yml
admin_pw: "..."
```

Put the password and save
