"""
Tests for WebhookIPValidator.
"""

import pytest

from aioyookassa.core.webhook_validator import WebhookIPValidator
from aioyookassa.exceptions.webhooks import InvalidWebhookIPError


class TestWebhookIPValidator:
    """Test WebhookIPValidator."""

    def test_default_allowed_ips(self):
        """Test that default YooKassa IPs are allowed."""
        validator = WebhookIPValidator()

        # Test some IPs from default ranges
        assert validator.is_allowed("185.71.76.1") is True
        assert validator.is_allowed("185.71.77.1") is True
        assert validator.is_allowed("77.75.156.11") is True
        assert validator.is_allowed("77.75.156.35") is True

    def test_custom_allowed_ips(self):
        """Test validator with custom IP list."""
        validator = WebhookIPValidator(allowed_ips=["192.168.1.1", "10.0.0.0/24"])

        assert validator.is_allowed("192.168.1.1") is True
        assert validator.is_allowed("10.0.0.1") is True
        assert validator.is_allowed("10.0.0.255") is True
        assert validator.is_allowed("185.71.76.1") is False  # Not in custom list

    def test_ipv6_support(self):
        """Test IPv6 address validation."""
        validator = WebhookIPValidator()

        # Test IPv6 from default range
        assert validator.is_allowed("2a02:5180::1") is True
        assert validator.is_allowed("2a02:5180:0:0:0:0:0:1") is True

    def test_invalid_ip(self):
        """Test that invalid IPs are rejected."""
        validator = WebhookIPValidator()

        assert validator.is_allowed("invalid") is False
        assert validator.is_allowed("999.999.999.999") is False
        assert validator.is_allowed("") is False

    def test_unauthorized_ip(self):
        """Test that unauthorized IPs are rejected."""
        validator = WebhookIPValidator()

        assert validator.is_allowed("8.8.8.8") is False
        assert validator.is_allowed("1.1.1.1") is False
        assert validator.is_allowed("192.168.1.1") is False

    def test_cidr_range(self):
        """Test CIDR range validation."""
        validator = WebhookIPValidator(allowed_ips=["192.168.1.0/24"])

        assert validator.is_allowed("192.168.1.1") is True
        assert validator.is_allowed("192.168.1.100") is True
        assert validator.is_allowed("192.168.1.255") is True
        assert validator.is_allowed("192.168.2.1") is False  # Outside range

    def test_empty_allowed_ips(self):
        """Test validator with empty allowed IPs list."""
        validator = WebhookIPValidator(allowed_ips=[])

        assert validator.is_allowed("185.71.76.1") is False
        assert validator.is_allowed("any_ip") is False

    def test_invalid_ip_in_allowed_list(self):
        """Test that invalid IPs in allowed_ips are silently skipped."""
        # Validator should skip invalid IPs and continue
        validator = WebhookIPValidator(
            allowed_ips=["192.168.1.1", "invalid_ip", "10.0.0.0/24", "also_invalid"]
        )

        # Valid IPs should still work
        assert validator.is_allowed("192.168.1.1") is True
        assert validator.is_allowed("10.0.0.1") is True

        # Invalid IPs should be rejected
        assert validator.is_allowed("invalid_ip") is False
        assert validator.is_allowed("also_invalid") is False
