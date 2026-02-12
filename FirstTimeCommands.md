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

## Mount external SSD to Raspberry PI

Format the drive to use `ext4`.

Plug in via USB (take fastest possible interface)

```cmd
sudo blkid # get the uuid of the drive

### gives something like -> we want the "UUID" (not "PARTUUID")
### /dev/sda1: LABEL="kubernetes-data" UUID="05520912-6cfa-4185-8f26-8d00f54fcaa4" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="6f1f1002-03f3-4561-935c-e2d788bcdaf7"

sudo mkdir /kubernetes-data
sudo nano /etc/fstab

# add this line to the bottom (we want boot to fail if it is missing)

UUID=05520912-6cfa-4185-8f26-8d00f54fcaa4  /kubernetes-data  ext4  defaults,noatime  0  2

# test config
sudo mount -a
sudo systemctl daemon-reload
sudo mount -a

# DO NOT REBOOT IF ERRORS APPEAR, IT WILL NOT COME BACK!

# Set filesystem permissions https://chmod-calculator.com/

sudo chown root:root /kubernetes-data
sudo chmod 755 /kubernetes-data
```

## Test speed of a disk

USB negotiation check:

- 5000M → USB 3 (correct)
- 480M → USB 2 (bottleneck)

```cmd
lsusb -t
```

Direct Benchmark (write)

```cmd
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches
dd if=/dev/zero of=benchfile bs=1G count=1 oflag=direct status=progress
```

Direct Benchmark (read)

```cmd
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches
dd if=benchfile of=/dev/null bs=1G iflag=direct status=progress
```

Cleanup

```cmd
rm benchfile
```
