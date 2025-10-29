"""
Tests for core utilities.
"""

import uuid

import pytest

from aioyookassa.core.utils import generate_idempotence_key


class TestGenerateIdempotenceKey:
    """Test generate_idempotence_key function."""

    def test_generate_idempotence_key_returns_string(self):
        """Test that generate_idempotence_key returns a string."""
        key = generate_idempotence_key()
        assert isinstance(key, str)

    def test_generate_idempotence_key_returns_uuid(self):
        """Test that generate_idempotence_key returns a valid UUID."""
        key = generate_idempotence_key()
        # Should be able to parse as UUID
        uuid.UUID(key)

    def test_generate_idempotence_key_unique(self):
        """Test that generate_idempotence_key returns unique values."""
        keys = [generate_idempotence_key() for _ in range(100)]
        # All keys should be unique
        assert len(set(keys)) == 100

    def test_generate_idempotence_key_format(self):
        """Test that generate_idempotence_key returns proper UUID format."""
        key = generate_idempotence_key()
        # UUID4 format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
        assert len(key) == 36  # 32 hex chars + 4 hyphens
        assert key.count("-") == 4
        assert all(c in "0123456789abcdef-" for c in key.lower())

    def test_generate_idempotence_key_multiple_calls(self):
        """Test multiple calls to generate_idempotence_key."""
        keys = []
        for _ in range(10):
            key = generate_idempotence_key()
            keys.append(key)
            # Each key should be a valid UUID
            uuid.UUID(key)

        # All keys should be different
        assert len(set(keys)) == 10

