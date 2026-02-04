# Ionos VPS Config

LEW NAT traversal and High performance

- vps 4 4 120
- Add an IPV6 address
- Firewall Rules
  - Either
    - Edit so that the TCP Ports that are free are
    - `22, 80, 443, 8123`
  - Alternatively, you could activate a firewall rule that
    - `TCP: 1-65535 | UDP: 1-65535`
    - As we activate a proper firewall on the server itself, that dynamically opens the required ports
