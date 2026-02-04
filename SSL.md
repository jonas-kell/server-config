# SSL

Ionos:

- Generate Certificate
  - Thereby a private key file is being downloaded
    -> ssl_certificate_key `/secrets/privkey.pem`
- Wait for it to be issued
  - Now Download the Certificate and the Intermediate
  - Append FIRST Certificate and THEN Intermediate(s) into
    -> ssl_certificate `/secrets/fullchain.pem`

## Ansible

In this case, the files are stored with ansible vault

```cmd
ansible-vault encrypt secrets/privkey.pem
ansible-vault encrypt secrets/fullchain.pem
```

Store the password to a file

```cmd
mkdir -p ~/.ansible
chmod 700 ~/.ansible
echo 'your-vault-password' > ~/.ansible/vault_pass.txt
chmod 600 ~/.ansible/vault_pass.txt
```
