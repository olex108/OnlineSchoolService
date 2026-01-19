from unittest import TestCase

from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from courses.models import Course
from users.models import User

from users.src.transfer_api_service import StripeAPIService

import pytest
from unittest.mock import MagicMock, patch


class StripeAPIServiceTest(TestCase):
    def setUp(self):
        self.test_api_key = "1234qwer"
        self.stripe_service = StripeAPIService(self.test_api_key)

        self.user = User.objects.create(email="test_user@test.com", password="test_PASSWORD", is_active=True)

        self.course = Course.objects.create(
            id=1,
            name="Test Course",
            description="Test Course",
            preview="",
            price=100.0,
            owner=self.user,
            stripe_product_id=None
        )

    @patch("stripe.Price.create")
    @patch("stripe.checkout.Session.create")
    @patch.object(StripeAPIService, "create_product")
    def test_stripe_api(self, mock_create_prod, mock_session_create, mock_price_create):

        mock_create_prod.return_value = {"id": "prod_new_456"}
        mock_price_create.return_value = {"id": "price_456"}
        mock_session_create.return_value = {"id": "sess_456", "url": "https://stripe.com/new"}

        result = self.stripe_service.create_transfer_and_return_data(self.course, 100.0)

        assert result["product_id"] == "prod_new_456"
        assert result["price_id"] == "price_456"
        assert result["session_id"] == "sess_456"
        assert result["link"] == "https://stripe.com/new"
        assert self.course.stripe_product_id == "prod_new_456"
