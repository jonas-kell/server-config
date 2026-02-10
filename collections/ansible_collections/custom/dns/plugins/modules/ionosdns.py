#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import aiohttp
from typing import Literal, Optional, Dict


DOCUMENTATION = r"""
---
module: ionos
short_description: Update DNS settings on Ionos DNS API
description:
  - Update DNS settings on Ionos DNS API
options:
  prefix:
    description: "Prefix part of the API credentials. See: https://developer.hosting.ionos.de/keys"
    type: str
    required: true
  key:
    description: "Secret key part of the API credentials. See: https://developer.hosting.ionos.de/keys"
    type: str
    required: true
  zone_domain:
    description: "The domain that the DNS control panel is registered under"
    type: str
    required: true
  domain:
    description: "The exact domain of which the settings should be applied to"
    type: str
    required: true
  target_ipv6_address:
    description: "The ipv6 address that the DNS entry should be set to"
    type: str
    required: true
  timeout:
    description: "API timeout in seconds"
    type: int
    default: 10 
  log_http_traffic:
    description: "Whether to log the http traffic and details"
    type: bool
    default: false 
author:
  - Jonas Kell
"""

EXAMPLES = r"""
- name: Change DNS settings
  custom.dns.ionos:
    prefix: "llllllllhhhhhhhhaaaaaaaadddddddd"
    ...
"""

RETURN = r"""
result:
  description: Ionos DNS upadte result
  type: dict
  returned: always
  sample:
    old_ip: "2606:50c0:8001:0:0:0:0:153"
    new_ip: "2a02:f90:e183:ee00:3202:1a40:5f5c:ced"
    changed: true
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            prefix=dict(type="str", required=True),
            key=dict(type="str", required=True),
            zone_domain=dict(type="str", required=True),
            domain=dict(type="str", required=True),
            target_ipv6_address=dict(type="str", required=True),
            timeout=dict(type="int", default=10),
            log_http_traffic=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    params = module.params

    api_prefix = params["prefix"]
    api_key = params["key"]
    zone_domain = params["zone_domain"]
    domain = params["domain"]
    target_ipv6_address = params["target_ipv6_address"]
    timout = params["timeout"]
    log_http_traffic = params["log_http_traffic"]

    # module.fail_json(msg="count must be >= 0")

    old_ip = "temp"
    new_ip = "temp"

    module.exit_json(changed=True, old_ip=old_ip, new_ip=new_ip)


if __name__ == "__main__":
    main()


class DNSUpdater:
    def __init__(self, log_http_errors: bool, timeout: int) -> None:
        self._log_http_errors = log_http_errors
        self._timeout = timeout

    async def update_ipv6_address_entry(self) -> bool:
        return False

    async def request(
        self,
        url: str,
        call_type: Literal["GET", "PUT"],
        headers: Dict[str, str],
        body: Optional[str],
    ):
        status_code = 0
        json = {}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                if call_type == "GET":
                    async with session.get(url, timeout=self._timeout) as resp:
                        status_code = resp.status
                        if status_code == 200 or status_code == 201:
                            json = await resp.json()
                elif call_type == "PUT":
                    async with session.put(
                        url, timeout=self._timeout, data=body
                    ) as resp:
                        status_code = resp.status
                        if status_code == 200 or status_code == 201:
                            json = await resp.json()

        except Exception as ex:
            if self._log_http_errors:
                print(
                    f"Could not connect to DNS update API because of  {type(ex).__name__}, {str(ex.args)}"
                )
            return False, {}

        if status_code != 200 and status_code != 201:
            print(
                f"Could connect to DNS update API but returned status code {status_code} {json}"
            )
            return False, {}

        return True, json


class IonosDNSUpdater(DNSUpdater):
    _domain: str
    _zone_domain: str
    _encryption: str
    _prefix: str
    _auth_header_key: str
    _auth_header: str
    _zone_id: Optional[str]
    _record_id: Optional[str]
    _attempt_update: bool
    _time_to_live: int

    def __init__(self, domain: str, log_http_errors: bool, timeout: int) -> None:
        super().__init__(log_http_errors, timeout)

        self._domain = domain
        self._zone_domain = zone_domain
        self._dns_sensor = dns_sensor
        self._local_sensor = local_sensor
        self._encryption = encryption
        self._prefix = prefix
        self._time_to_live = time_to_live

        self._auth_header_key = "X-API-Key"
        self._auth_header = f"{self._prefix}.{self._encryption}"

        self._zone_id = None
        self._record_id = None
        self._attempt_update = (
            self._zone_domain != "" and self._encryption != "" and self._prefix != ""
        )
        if self._attempt_update:
            await self.initialize_ids()
        else:
            _LOGGER.warning(
                f"Some of the Update-required properties are not set. Therefore dns updater integration only provides the sensors in read mode."
            )

    async def initialize_ids(self) -> None:
        # INIT the zone and record id
        got_all = False
        try:
            result_zones_success, result_zones_lookup = await self.request(
                "https://api.hosting.ionos.com/dns/v1/zones",
                "GET",
                {self._auth_header_key: self._auth_header},
                None,
            )
            if result_zones_success:
                for result_zone_obj in result_zones_lookup:
                    if result_zone_obj["name"] == self._zone_domain:
                        self._zone_id = result_zone_obj["id"]

                if self._zone_id is None:
                    print(
                        f"Did not find the zone id to the zone_domain value {self._zone_domain}"
                    )
                else:
                    result_records_success, result_records_lookup = await self.request(
                        f"https://api.hosting.ionos.com/dns/v1/zones/{self._zone_id}",
                        "GET",
                        {self._auth_header_key: self._auth_header},
                        None,
                    )
                    if result_records_success:
                        for result_record_obj in result_records_lookup["records"]:
                            if (
                                result_record_obj["name"] == self._domain
                                and result_record_obj["type"] == "AAAA"
                            ):
                                self._record_id = result_record_obj["id"]
                                got_all = True
        except Exception as ex:
            print(f"Parsing exception {type(ex).__name__}, {str(ex.args)}")

        if not got_all:
            print(f"DNS updater initialization never found all necessary ids")

    async def update_ipv6_address_entry(self) -> bool:
        _LOGGER.info(f"Checking for necessary update of ipv6 address")

        if not self._attempt_update:
            return False
        if self._zone_id is None or self._record_id is None:
            _LOGGER.error(
                f"Tried to update, but either _zone_id or _record_id are none..."
            )

        local_address = IPv6Address(self._local_sensor.native_value)
        dns_address = IPv6Address(self._dns_sensor.native_value)
        local_address_short = str(local_address.compressed)
        dns_address_short = str(dns_address.compressed)

        if local_address_short != dns_address_short:
            # differs, should be updated
            _LOGGER.info(
                f"Attempting update of DNS entry on IONOS API from {dns_address_short} -> {local_address_short}"
            )
            status, _ = await self.request(
                f"https://api.hosting.ionos.com/dns/v1/zones/{self._zone_id}/records/{self._record_id}",
                "PUT",
                {
                    self._auth_header_key: self._auth_header,
                    "Content-Type": "application/json",
                },
                f'{{"disabled": false, "content": "{local_address_short}", "ttl": {self._time_to_live}, "prio": 0}}',
            )
            if status:
                _LOGGER.info(
                    f"Used the IONOS DNS API to set the AAAA entry for {self._domain} to {local_address_short}"
                )

                # update the sensor value
                self._dns_sensor._previous_native_value = self._dns_sensor._native_value
                self._dns_sensor._native_value = local_address_short

            return status
        _LOGGER.info(f"Adresses are both {dns_address_short} no update necessary")
        return False
