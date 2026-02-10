#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import aiohttp
import asyncio
from typing import Literal, Optional, Dict, List, Tuple


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
  entry_ttl:
    description: "TTL parameter to set on the entry (in s)"
    type: int
    default: 300
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


class APIInteractor:
    _logs: List[str]

    def __init__(self, log_http_errors: bool, timeout: int) -> None:
        self._log_http_errors = log_http_errors
        self._timeout = timeout
        self._logs = []

    def log_print(self, line: str):
        self._logs.append(line)

    def get_logs(self) -> List[str]:
        return self._logs

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
                self.log_print(
                    f"Could not connect to DNS update API because of  {type(ex).__name__}, {str(ex.args)}"
                )
            return False, {}

        if status_code != 200 and status_code != 201:
            self.log_print(
                f"Could connect to DNS update API but returned status code {status_code} {json}"
            )
            return False, {}

        return True, json


class IonosDNSUpdater(APIInteractor):
    _zone_domain: str
    _domain: str
    _encryption: str
    _prefix: str
    _auth_header_key: str
    _auth_header: str
    _zone_id: Optional[str]
    _record_id: Optional[str]
    _can_attempt_update: bool
    _time_to_live: int

    def __init__(
        self,
        zone_domain: str,
        domain: str,
        prefix: str,
        encryption: str,
        log_http_errors: bool,
        timeout: int,
        time_to_live: int,
    ) -> None:
        super().__init__(log_http_errors, timeout)

        self._zone_domain = zone_domain
        self._domain = domain
        self._prefix = prefix
        self._encryption = encryption
        self._time_to_live = time_to_live

        self._auth_header_key = "X-API-Key"
        self._auth_header = f"{self._prefix}.{self._encryption}"

        self._zone_id = None
        self._record_id = None
        self._can_attempt_update = (
            self._zone_domain != "" and self._encryption != "" and self._prefix != ""
        )

    async def async_init(self) -> bool:
        if self._can_attempt_update:
            await self.initialize_ids()
            return True
        else:
            self.log_print(
                "Some of the Update-required properties are not set. Therefore dns updater can not do stuff"
            )
            return False

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
                    self.log_print(
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
            self.log_print(f"Parsing exception {type(ex).__name__}, {str(ex.args)}")

        if not got_all:
            self.log_print(f"DNS updater initialization never found all necessary ids")

        return got_all

    async def get_ipv6_address_entry(self) -> Tuple[bool, str | None]:
        if not self._can_attempt_update:
            self.log_print("API interactor not properly initialized")
            return (False, None)

        if self._zone_id is None or self._record_id is None:
            self.log_print(
                "Called request function, but either _zone_id or _record_id are None ..."
            )
            return (False, None)

        status, result = await self.request(
            f"https://api.hosting.ionos.com/dns/v1/zones/{self._zone_id}/records/{self._record_id}",
            "GET",
            {
                self._auth_header_key: self._auth_header,
                "Content-Type": "application/json",
            },
            None,
        )
        if status:
            self.log_print(
                f"Used the IONOS DNS API to get the AAAA entry for {self._domain}: {result}"
            )
            return (status, result.get("content"))

        self.log_print("API did not return success, when getting AAAA entry")
        return (False, None)

    async def update_ipv6_address_entry(self, new_ip: str) -> bool:
        if not self._can_attempt_update:
            self.log_print("API interactor not properly initialized")
            return False

        if self._zone_id is None or self._record_id is None:
            self.log_print(
                "Called update function, but either _zone_id or _record_id are None ..."
            )
            return False

        status, _ = await self.request(
            f"https://api.hosting.ionos.com/dns/v1/zones/{self._zone_id}/records/{self._record_id}",
            "PUT",
            {
                self._auth_header_key: self._auth_header,
                "Content-Type": "application/json",
            },
            f'{{"disabled": false, "content": "{new_ip}", "ttl": {self._time_to_live}, "prio": 0}}',
        )
        if status:
            self.log_print(
                f"Used the IONOS DNS API to set the AAAA entry for {self._domain} to {new_ip}"
            )

        return status


async def main():
    module = AnsibleModule(
        argument_spec=dict(
            prefix=dict(type="str", required=True),
            key=dict(type="str", required=True),
            zone_domain=dict(type="str", required=True),
            domain=dict(type="str", required=True),
            target_ipv6_address=dict(type="str", required=True),
            timeout=dict(type="int", default=10),
            entry_ttl=dict(type="int", default=300),
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
    entry_ttl = params["entry_ttl"]
    timeout = params["timeout"]
    log_http_traffic = params["log_http_traffic"]

    ionos_api_interactor = IonosDNSUpdater(
        zone_domain=zone_domain,
        domain=domain,
        encryption=api_key,
        prefix=api_prefix,
        log_http_errors=log_http_traffic,
        time_to_live=entry_ttl,
        timeout=timeout,
    )

    init_state = await ionos_api_interactor.async_init()
    if not init_state:
        module.fail_json(
            msg="Could not initialize Ionos API interactor",
            logs=ionos_api_interactor.get_logs(),
        )

    id_init_state = await ionos_api_interactor.initialize_ids()
    if not id_init_state:
        module.fail_json(
            msg="Could not gather Ionos API ids",
            logs=ionos_api_interactor.get_logs(),
        )

    (before_update_state, before_update_ip) = (
        await ionos_api_interactor.get_ipv6_address_entry()
    )
    if not before_update_state:
        module.fail_json(
            msg="Could not read from Ionos API",
            logs=ionos_api_interactor.get_logs(),
        )

    if before_update_ip == target_ipv6_address:
        module.exit_json(
            changed=False,
            old_ip=before_update_ip,
            new_ip=target_ipv6_address,
            logs=ionos_api_interactor.get_logs(),
        )

    update_state = await ionos_api_interactor.update_ipv6_address_entry(
        new_ip=target_ipv6_address
    )
    if not update_state:
        module.fail_json(
            msg="Could not write to Ionos API",
            logs=ionos_api_interactor.get_logs(),
        )

    (after_update_state, after_update_ip) = (
        await ionos_api_interactor.get_ipv6_address_entry()
    )
    if not after_update_state:
        module.fail_json(
            msg="Could not read from Ionos API (after update)",
            logs=ionos_api_interactor.get_logs(),
        )

    if after_update_ip == target_ipv6_address:
        module.exit_json(
            changed=True,
            old_ip=before_update_ip,
            new_ip=after_update_ip,
            logs=ionos_api_interactor.get_logs(),
        )

    module.fail_json(
        changed=True,  # assume something was wrecked
        msg="The change was not applied correctly as it seemes",
        logs=ionos_api_interactor.get_logs(),
    )


if __name__ == "__main__":
    asyncio.run(main())
