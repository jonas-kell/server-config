# Pihole documentation and Notes

If you want to use Pihole.

It is included as a Deployment in the k3s cluster, started by [Piserver](./playbooks/piserver.yml).

You need to perform `Disable the default DNS` in [First Time Commands](./FirstTimeCommands.md)!

## How to get better Blocklists

[Find them here](https://github.com/hagezi/dns-blocklists)

Should probably use `Multi-Normal`

There is `Link` in the category that contains Pihole (Adblock).

Add under Lists -> Add new Subscribed List -> Paste Link -> `Add BLOCKLIST`

Then Tools -> Update Gravity

## Static IPv6 address

To use the DNS server in LAN with IPv6, we need a static unique-local-address

```cmd
GLOBAL_ID=$(openssl rand -hex 5)  # e.g., "f8e45a7a73"
ULA_PREFIX="fd${GLOBAL_ID:0:2}:${GLOBAL_ID:2:4}:${GLOBAL_ID:6:2}00"
ULA_IP="$ULA_PREFIX::1/64"
echo "Your ULA_IP is: $ULA_IP"

# Or use https://unique-local-ipv6.com/#
# Add it in the piserver

sudo ip -6 addr add "$ULA_IP" dev eth0
```

Set it in the router

- Network -> Settings -> Networks -> Default -> IPv6 -> Advanced -> DNS Server
  - Full with ::1, not the /64

Make Other Devices get such a Unique Local IP:

- Network -> Settings -> Networks -> Default -> IPv6 -> Additional IPs
  - Enter IPv6 CIDR -> add the full IP with the ::1/64 (the one gets cut because of the /64, the /64 is needed)
