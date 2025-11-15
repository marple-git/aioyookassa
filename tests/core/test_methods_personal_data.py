"""
Tests for personal data methods.
"""

from datetime import date, datetime

import pytest

from aioyookassa.core.methods.personal_data import (
    CreatePersonalData,
    GetPersonalData,
    PersonalDataAPIMethod,
)


class TestPersonalDataAPIMethod:
    """Test PersonalDataAPIMethod base class."""

    def test_personal_data_api_method_initialization(self):
        """Test PersonalDataAPIMethod initialization."""
        method = PersonalDataAPIMethod()
        assert method.http_method == "GET"
        assert method.path == "/personal_data"

    def test_personal_data_api_method_with_custom_path(self):
        """Test PersonalDataAPIMethod with custom path."""
        method = PersonalDataAPIMethod(path="/custom/path")
        assert method.path == "/custom/path"

    def test_personal_data_api_method_build(self):
        """Test PersonalDataAPIMethod build method."""
        method = PersonalDataAPIMethod.build("pd_123")
        assert method.path == "/personal_data"  # Should use class path

    def test_personal_data_api_method_build_with_format(self):
        """Test PersonalDataAPIMethod build with path formatting."""

        class TestMethod(PersonalDataAPIMethod):
            path = "/personal_data/{personal_data_id}"

        method = TestMethod.build("pd_123")
        assert method.path == "/personal_data/pd_123"


class TestCreatePersonalData:
    """Test CreatePersonalData method."""

    def test_create_personal_data_initialization(self):
        """Test CreatePersonalData initialization."""
        method = CreatePersonalData()
        assert method.http_method == "POST"
        assert method.path == "/personal_data"

    def test_create_personal_data_build_params_sbp_type(self):
        """Test CreatePersonalData build_params with SBP type."""
        params = CreatePersonalData.build_params(
            type="sbp_payout_recipient",
            last_name="Ivanov",
            first_name="Ivan",
            middle_name="Ivanovich",
        )

        assert params["type"] == "sbp_payout_recipient"
        assert params["last_name"] == "Ivanov"
        assert params["first_name"] == "Ivan"
        assert params["middle_name"] == "Ivanovich"
        assert "birthdate" not in params

    def test_create_personal_data_build_params_statement_type(self):
        """Test CreatePersonalData build_params with statement type."""
        birthdate = date(1990, 1, 15)
        params = CreatePersonalData.build_params(
            type="payout_statement_recipient",
            last_name="Petrov",
            first_name="Petr",
            middle_name="Petrovich",
            birthdate=birthdate,
        )

        assert params["type"] == "payout_statement_recipient"
        assert params["last_name"] == "Petrov"
        assert params["first_name"] == "Petr"
        assert params["middle_name"] == "Petrovich"
        assert params["birthdate"] == "1990-01-15"

    def test_create_personal_data_build_params_with_datetime_birthdate(self):
        """Test CreatePersonalData build_params with datetime birthdate."""
        birthdate = datetime(1990, 1, 15, 12, 30, 0)
        params = CreatePersonalData.build_params(
            type="payout_statement_recipient",
            last_name="Sidorov",
            first_name="Sidor",
            birthdate=birthdate,
        )

        assert params["birthdate"] == "1990-01-15T12:30:00"

    def test_create_personal_data_build_params_with_string_birthdate(self):
        """Test CreatePersonalData build_params with string birthdate."""
        params = CreatePersonalData.build_params(
            type="payout_statement_recipient",
            last_name="Kuznetsov",
            first_name="Kuzma",
            birthdate="1990-01-15",
        )

        assert params["birthdate"] == "1990-01-15"

    def test_create_personal_data_build_params_with_metadata(self):
        """Test CreatePersonalData build_params with metadata."""
        params = CreatePersonalData.build_params(
            type="sbp_payout_recipient",
            last_name="Ivanov",
            first_name="Ivan",
            metadata={"key": "value", "order_id": "12345"},
        )

        assert params["metadata"] == {"key": "value", "order_id": "12345"}

    def test_create_personal_data_build_params_filters_none_values(self):
        """Test CreatePersonalData build_params filters out None values."""
        params = CreatePersonalData.build_params(
            type="sbp_payout_recipient",
            last_name="Ivanov",
            first_name="Ivan",
            middle_name=None,
            birthdate=None,
            metadata=None,
        )

        assert params["type"] == "sbp_payout_recipient"
        assert params["last_name"] == "Ivanov"
        assert params["first_name"] == "Ivan"
        assert "middle_name" not in params
        assert "birthdate" not in params
        assert "metadata" not in params


class TestGetPersonalData:
    """Test GetPersonalData method."""

    def test_get_personal_data_initialization(self):
        """Test GetPersonalData initialization."""
        method = GetPersonalData()
        assert method.http_method == "GET"
        assert method.path == "/personal_data/{personal_data_id}"

    def test_get_personal_data_build(self):
        """Test GetPersonalData build method."""
        method = GetPersonalData.build("pd_123")
        assert method.path == "/personal_data/pd_123"
