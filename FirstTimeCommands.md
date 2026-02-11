# First time commands (setup)

This should only be necessary to be ran once, not regularily

## Set root Password, Enable SSH

```cmd
sudo passwd

sudo apt get update
sudo apt get install openssh-server
```

## Passwordless SUDO

```cmd
sudo visudo

# Add line AT THE END

pi ALL=(ALL:ALL) NOPASSWD: ALL
```

## Disable SSH login via password

```cmd
sudo nano /etc/ssh/sshd_config

# modify or add

PasswordAuthentication no
ChallengeResponseAuthentication no
PubkeyAuthentication yes
PermitRootLogin prohibit-password

# then

sudo service ssh restart
systemctl daemon-reload
```

Test with (should work beforehand, no longer after):

```cmd
ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no ...
```
