# Backups !!!

This needs to be automated WAAAAY more!

## Manual backup of 'kubernetes-data'

```cmd
sudo /usr/local/bin/k3s-killall.sh # stop cluster

sudo su
rsync -aHAX --info=progress2 /kubernetes-data/k3s/ /pi-data-backup/k3s-$(date +%F-%H%M)/
exit

sudo systemctl start k3s
```
