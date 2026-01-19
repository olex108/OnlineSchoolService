from unittest.mock import patch

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from courses.models import Course
from users.models import User
from users.src.transfer_api_service import StripeAPIService
from users.views import PaymentCreateAPIView


class PaymentTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email="test_user@test.com", password="test_PASSWORD", is_active=True)
        self.course = Course.objects.create(
            id=1,
            name="test_course",
            preview="",
            video_url="",
            owner=self.user,
            description="test_course_description",
            price=1000,
        )
        self.course_free = Course.objects.create(
            id=2,
            name="test_free_course",
            preview="",
            video_url="",
            owner=self.user,
            description="test_course_description",
            price=None,
        )

    def test_create_payment_cash(self):
        view = PaymentCreateAPIView.as_view()
        request = self.factory.post(
            "/payments/create/",
            data={
                "paid_course": self.course.id,
                "paid_lesson": "",
                "payment_method": "CASH",
            },
            format="json",
        )

        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["paid_course"], self.course.id)
        self.assertEqual(response.data["amount"], self.course.price)
        self.assertEqual(response.data["transfer"], None)

        request = self.factory.post(
            "/payments/create/",
            data={
                "paid_course": self.course_free.id,
                "paid_lesson": "",
                "payment_method": "CASH",
            },
            format="json",
        )

        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, [ErrorDetail(string="Данный курс бесплатный", code="invalid")])

    @patch.object(StripeAPIService, "create_transfer_and_return_data")
    def test_create_payment_transfer(self, moch_create_stripe):

        moch_data_dict = {
            "link": "https://stripe.com/new",
            "session_id": "sess_456",
            "price_id": "price_456",
            "product_id": "prod_new_456",
        }

        moch_create_stripe.return_value = moch_data_dict

        view = PaymentCreateAPIView.as_view()
        request = self.factory.post(
            "/payments/create/",
            data={
                "paid_course": self.course.id,
                "paid_lesson": "",
                "payment_method": "TRANSFER",
            },
            format="json",
        )

        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["transfer"]["link"], moch_data_dict["link"])
        self.assertEqual(response.data["transfer"]["session_id"], moch_data_dict["session_id"])
        self.assertEqual(response.data["transfer"]["price_id"], moch_data_dict["price_id"])
        self.assertEqual(response.data["transfer"]["product_id"], moch_data_dict["product_id"])
