# How to configure the Unifi OS details

## Configure Forwardings to make services reachable

Generate IPV6 net-groups

- Settings -> Overview -> Network Lists
  - IPv6 Address/Subnet
    - Add one for Home Assistant
    - Add one for Local Server

Delete all port forwardings

- Settings -> Policy Engine -> Zones

Adapt Internet v6 rules

- Add Rule
  - Source: External: Any, Any
  - Action: Allow
  - Destination: Internal -> IP -> List -> Created List
  - IP Version: IPv6

Add a policy with name `debug-reevaluate` to be able to trigger re-evaluation of firewall rules
(it can do just nothing or allow traffic from and to the same IP (effectively does nothing))

## Setting values

The values for these entries get set by [this ansible script](./playbooks/unifi_ipv6_firewall_config.yml)

## DNS Server

See configurations in the [Pihole](./Pihole.md) explanation
