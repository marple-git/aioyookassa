"""
IP address validator for YooKassa webhook notifications.
"""

import ipaddress
import logging
from typing import List, Optional, Set, Union

logger = logging.getLogger(__name__)


class WebhookIPValidator:
    """
    Validator for YooKassa webhook IP addresses.

    Validates that incoming webhook requests come from authorized YooKassa IP ranges.
    Supports both IPv4 and IPv6 addresses, CIDR ranges, and individual IPs.
    """

    # Official YooKassa IP ranges
    DEFAULT_ALLOWED_IPS: List[str] = [
        "185.71.76.0/27",
        "185.71.77.0/27",
        "77.75.153.0/25",
        "77.75.156.11",
        "77.75.156.35",
        "77.75.154.128/25",
        "2a02:5180::/32",
    ]

    def __init__(
        self,
        allowed_ips: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize IP validator.

        :param allowed_ips: List of allowed IP addresses or CIDR ranges.
                            If None, uses default YooKassa IP ranges.
        :param logger: Logger instance. If None, uses default logger.
        """
        self.logger = logger if logger is not None else logging.getLogger(__name__)
        self._allowed_networks: Set[
            Union[ipaddress.IPv4Network, ipaddress.IPv6Network]
        ] = set()
        self._allowed_ips: Set[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]] = (
            set()
        )

        ips_to_use = (
            allowed_ips if allowed_ips is not None else self.DEFAULT_ALLOWED_IPS
        )
        self._parse_allowed_ips(ips_to_use)
        self.logger.debug(
            f"Initialized IP validator with {len(self._allowed_networks)} networks "
            f"and {len(self._allowed_ips)} individual IPs"
        )

    def _parse_allowed_ips(self, allowed_ips: List[str]) -> None:
        """Parse and store allowed IP addresses and networks."""
        for ip_str in allowed_ips:
            try:
                # Try to parse as network (CIDR)
                if "/" in ip_str:
                    network = ipaddress.ip_network(ip_str, strict=False)
                    self._allowed_networks.add(network)
                else:
                    # Parse as individual IP
                    ip_addr = ipaddress.ip_address(ip_str)
                    self._allowed_ips.add(ip_addr)
            except ValueError:
                # Invalid IP format, skip it
                continue

    def is_allowed(self, ip: str) -> bool:
        """
        Check if IP address is allowed.

        :param ip: IP address to check (IPv4 or IPv6).
        :return: True if IP is allowed, False otherwise.
        """
        try:
            ip_addr = ipaddress.ip_address(ip)
        except ValueError:
            # Invalid IP format
            self.logger.warning(f"Invalid IP address format: {ip}")
            return False

        # Check individual IPs first
        if ip_addr in self._allowed_ips:
            self.logger.debug(f"IP {ip} is allowed (individual IP match)")
            return True

        # Check networks
        for network in self._allowed_networks:
            if ip_addr in network:
                self.logger.debug(f"IP {ip} is allowed (network {network} match)")
                return True

        self.logger.warning(f"IP {ip} is not in whitelist")
        return False
