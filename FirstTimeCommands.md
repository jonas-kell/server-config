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
### /dev/sdb1: LABEL="pi-data-backup" UUID="0a569030-6399-47ed-972d-d51f7dc5c0fe" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="a84dd232-75d6-a245-9ec5-64b35e8f3f8b"

sudo mkdir /kubernetes-data
sudo chmod 000 /kubernetes-data # make mountpoint folder itself unwritable!! (in case drice is missing later)

sudo mkdir /pi-data-backup
sudo chmod 000 /pi-data-backup

sudo nano /etc/fstab

# add this line to the bottom (we want boot to fail if it is missing)

UUID=05520912-6cfa-4185-8f26-8d00f54fcaa4  /kubernetes-data  ext4  defaults,noatime,x-systemd.automount,nofail    0  2
UUID=0a569030-6399-47ed-972d-d51f7dc5c0fe  /pi-data-backup  ext4  defaults,noatime,x-systemd.automount,nofail    0  2

# test config
sudo mount -a
sudo systemctl daemon-reload
sudo mount -a

# DO NOT REBOOT IF ERRORS APPEAR, IT WILL NOT COME BACK!

# Set filesystem permissions https://chmod-calculator.com/ (AFTER mount, the folder is in fact a "different" folder. For that we set runtime permissions)

sudo chown root:root /kubernetes-data
sudo chmod 755 /kubernetes-data

sudo chown root:root /pi-data-backup
sudo chmod 755 /pi-data-backup
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

<!--
3.0 to USBC Adapter https://www.amazon.de/dp/B0FRLL3CWC?ref=ppx_yo2ov_dt_b_fed_asin_title
2.0 to USBC Adapter https://www.amazon.de/dp/B085VT1VJT?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1
SATA to 3.0 Adapter https://www.amazon.de/dp/B0FGRTW9BR?ref=ppx_yo2ov_dt_b_fed_asin_title
SATA to USBC 3.1 Adapter https://www.amazon.de/dp/B07KP9YK7T?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

Afterwards switched for this one: https://www.amazon.de/gp/product/B07NYC6LKB


USB 3.0 Adapter PI
w 174 MB/s
r 31,1 MB/s - 270 MB/s - 319 MB/s (sometimes fast, sometimes slow)

USB C over 3.0<->C Adapter (right way) PI
--- RANDOMLY STOPPED WORKING AT ALL IN THIS COMBINATION WHILE BENCHMARKING ---
--- worked for one try, then it just always died with that combination ---

USB C over 2.0<->C Adapter PI
w 29,6 MB/s
r 35,8 MB/s

USB 3.0 Over good USBc Hub
w 349 MB/s
r 420 MB/s

USB C over 3.0<->C Adapter (right way) Over good USBc Hub
w 351 MB/s
r 426 MB/s

USB C Adapter Over good USBc Hub
w 348 MB/s
r 423 MB/s

USB C over 3.0<->C Adapter (wrong way) Over good USBc Hub
w 40.7 MB/s
r 41.7 MB/s
 -->

## Switch to more stable USB driver (UAS -> usb-storage)

Necessary for ONLY incompatible USB-Sata adapters. 
[List of compatible adapters](https://forum-raspberrypi.de/forum/thread/47876-magische-usb-sata-adapter-und-wo-sie-zu-finden-sind/)

I now currently use [This one](https://www.amazon.de/gp/product/B07NYC6LKB) successfully.

```cmd
lsusb  # get id

## Bus 002 Device 005: ID 152d:0578 JMicron Technology Corp. / JMicron USA Technology Corp. JMS578 SATA 6Gb/s  ## USB-C SATA Adapter with 3.1 USBC Converter
## Bus 002 Device 006: ID 2109:0715 VIA Labs, Inc. VL817 SATA Adaptor ## this https://forum-raspberrypi.de/forum/thread/47876-magische-usb-sata-adapter-und-wo-sie-zu-finden-sind say that this https://www.amazon.de/gp/product/B07NYC6LKB performs good without quirks. This holds main kubernetes data at the moment

sudo nano /boot/firmware/cmdline.txt

# add to last line (must stay as one line!!):
# set id from step before
# (the USB adapter that needed this was https://www.amazon.de/dp/B0FGRTW9BR?ref=ppx_yo2ov_dt_b_fed_asin_title but is broke already and is apparently shit as it needs quirks)

usb-storage.quirks=7825:a2a4:u
```

## Disable the default DNS (if pihole is wanted)

See: [Pihole Docs](https://docs.pi-hole.net/docker/tips-and-tricks/)

```cmd
sudo lsof -i :53

# see the service that uses port 53
# if systemd-resolve:

sudo mkdir /etc/systemd/resolved.conf.d/
sudo nano /etc/systemd/resolved.conf.d/no-stub.conf

# enter:

[Resolve]
DNSStubListener=no

# up to here. Save and restart the service

sudo sh -c 'rm -f /etc/resolv.conf && ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf'


systemctl restart systemd-resolved
```
