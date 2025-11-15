"""
Tests for deals methods.
"""

from datetime import datetime

import pytest

from aioyookassa.core.methods.deals import CreateDeal, DealsAPIMethod, GetDeal, GetDeals
from aioyookassa.types.enum import DealStatus, FeeMoment


class TestDealsAPIMethod:
    """Test DealsAPIMethod base class."""

    def test_deals_api_method_initialization(self):
        """Test DealsAPIMethod initialization."""
        method = DealsAPIMethod()
        assert method.http_method == "GET"
        assert method.path == "/deals"

    def test_deals_api_method_with_custom_path(self):
        """Test DealsAPIMethod with custom path."""
        method = DealsAPIMethod(path="/custom/path")
        assert method.path == "/custom/path"

    def test_deals_api_method_build(self):
        """Test DealsAPIMethod build method."""
        method = DealsAPIMethod.build("deal_123")
        assert method.path == "/deals"  # Should use class path

    def test_deals_api_method_build_with_format(self):
        """Test DealsAPIMethod build with path formatting."""

        class TestMethod(DealsAPIMethod):
            path = "/deals/{deal_id}"

        method = TestMethod.build("deal_123")
        assert method.path == "/deals/deal_123"


class TestCreateDeal:
    """Test CreateDeal method."""

    def test_create_deal_initialization(self):
        """Test CreateDeal initialization."""
        method = CreateDeal()
        assert method.http_method == "POST"
        assert method.path == "/deals"

    def test_create_deal_build_params_minimal(self):
        """Test CreateDeal build_params with minimal data."""
        params = CreateDeal.build_params(fee_moment=FeeMoment.PAYMENT_SUCCEEDED)

        assert params["type"] == "safe_deal"
        assert params["fee_moment"] == FeeMoment.PAYMENT_SUCCEEDED
        assert "metadata" not in params
        assert "description" not in params

    def test_create_deal_build_params_with_all_fields(self):
        """Test CreateDeal build_params with all fields."""
        params = CreateDeal.build_params(
            fee_moment=FeeMoment.DEAL_CLOSED,
            description="Test deal description",
            metadata={"order_id": "12345", "customer_id": "67890"},
        )

        assert params["type"] == "safe_deal"
        assert params["fee_moment"] == FeeMoment.DEAL_CLOSED
        assert params["description"] == "Test deal description"
        assert params["metadata"] == {"order_id": "12345", "customer_id": "67890"}

    def test_create_deal_build_params_with_different_fee_moments(self):
        """Test CreateDeal build_params with different fee_moment values."""
        fee_moments = [FeeMoment.PAYMENT_SUCCEEDED, FeeMoment.DEAL_CLOSED]

        for fee_moment in fee_moments:
            params = CreateDeal.build_params(fee_moment=fee_moment)
            assert params["fee_moment"] == fee_moment

    def test_create_deal_build_params_filters_none_values(self):
        """Test CreateDeal build_params filters out None values."""
        params = CreateDeal.build_params(
            fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
            description=None,
            metadata=None,
        )

        assert params["type"] == "safe_deal"
        assert params["fee_moment"] == FeeMoment.PAYMENT_SUCCEEDED
        assert "description" not in params
        assert "metadata" not in params


class TestGetDeals:
    """Test GetDeals method."""

    def test_get_deals_initialization(self):
        """Test GetDeals initialization."""
        method = GetDeals()
        assert method.http_method == "GET"
        assert method.path == "/deals"

    def test_get_deals_build_params_minimal(self):
        """Test GetDeals build_params with minimal data."""
        params = GetDeals.build_params()

        assert params == {}

    def test_get_deals_build_params_with_created_at_filters(self):
        """Test GetDeals build_params with created_at filters."""
        created_at_gte = datetime(2023, 1, 1, 12, 0, 0)
        created_at_lte = datetime(2023, 1, 31, 23, 59, 59)

        params = GetDeals.build_params(
            created_at_gte=created_at_gte, created_at_lte=created_at_lte
        )

        assert "created_at.gte" in params
        assert "created_at.lte" in params
        assert params["created_at.gte"] == created_at_gte.isoformat()
        assert params["created_at.lte"] == created_at_lte.isoformat()

    def test_get_deals_build_params_with_expires_at_filters(self):
        """Test GetDeals build_params with expires_at filters."""
        expires_at_gte = datetime(2023, 1, 1, 12, 0, 0)
        expires_at_lt = datetime(2023, 1, 31, 23, 59, 59)

        params = GetDeals.build_params(
            expires_at_gte=expires_at_gte, expires_at_lt=expires_at_lt
        )

        assert "expires_at.gte" in params
        assert "expires_at.lt" in params
        assert params["expires_at.gte"] == expires_at_gte.isoformat()
        assert params["expires_at.lt"] == expires_at_lt.isoformat()

    def test_get_deals_build_params_with_all_filters(self):
        """Test GetDeals build_params with all filter types."""
        created_at_gte = datetime(2023, 1, 1, 12, 0, 0)
        created_at_gt = datetime(2023, 1, 2, 12, 0, 0)
        created_at_lte = datetime(2023, 1, 31, 23, 59, 59)
        created_at_lt = datetime(2023, 2, 1, 0, 0, 0)
        expires_at_gte = datetime(2023, 4, 1, 12, 0, 0)
        expires_at_gt = datetime(2023, 4, 2, 12, 0, 0)
        expires_at_lte = datetime(2023, 4, 30, 23, 59, 59)
        expires_at_lt = datetime(2023, 5, 1, 0, 0, 0)

        params = GetDeals.build_params(
            created_at_gte=created_at_gte,
            created_at_gt=created_at_gt,
            created_at_lte=created_at_lte,
            created_at_lt=created_at_lt,
            expires_at_gte=expires_at_gte,
            expires_at_gt=expires_at_gt,
            expires_at_lte=expires_at_lte,
            expires_at_lt=expires_at_lt,
            status=DealStatus.OPENED,
            full_text_search="test search",
            limit=50,
            cursor="next_cursor_123",
        )

        assert params["created_at.gte"] == created_at_gte.isoformat()
        assert params["created_at.gt"] == created_at_gt.isoformat()
        assert params["created_at.lte"] == created_at_lte.isoformat()
        assert params["created_at.lt"] == created_at_lt.isoformat()
        assert params["expires_at.gte"] == expires_at_gte.isoformat()
        assert params["expires_at.gt"] == expires_at_gt.isoformat()
        assert params["expires_at.lte"] == expires_at_lte.isoformat()
        assert params["expires_at.lt"] == expires_at_lt.isoformat()
        assert params["status"] == DealStatus.OPENED
        assert params["full_text_search"] == "test search"
        assert params["limit"] == 50
        assert params["cursor"] == "next_cursor_123"

    def test_get_deals_build_params_filters_none_values(self):
        """Test GetDeals build_params filters out None values."""
        params = GetDeals.build_params(
            created_at_gte=None,
            created_at_gt=None,
            status=None,
            full_text_search=None,
            limit=None,
            cursor=None,
        )

        assert params == {}

    def test_get_deals_build_params_with_status_filter(self):
        """Test GetDeals build_params with status filter."""
        params = GetDeals.build_params(status=DealStatus.CLOSED)

        assert params["status"] == DealStatus.CLOSED

    def test_get_deals_build_params_with_pagination(self):
        """Test GetDeals build_params with pagination."""
        params = GetDeals.build_params(limit=20, cursor="cursor_123")

        assert params["limit"] == 20
        assert params["cursor"] == "cursor_123"


class TestGetDeal:
    """Test GetDeal method."""

    def test_get_deal_initialization(self):
        """Test GetDeal initialization."""
        method = GetDeal()
        assert method.http_method == "GET"
        assert method.path == "/deals/{deal_id}"

    def test_get_deal_build(self):
        """Test GetDeal build method."""
        method = GetDeal.build("deal_123")
        assert method.path == "/deals/deal_123"
