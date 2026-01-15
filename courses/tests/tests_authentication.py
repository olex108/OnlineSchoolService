from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate

from courses.models import Course
from courses.views import CourseViewSet, LessonListAPIView
from users.models import Subscription, User
from users.views import SubscribeAPIView


class AuthenticationTest(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email="test_user@test.com", password="test_PASSWORD", is_active=True)

    def test_without_authentication(self):

        view = LessonListAPIView.as_view()
        request = self.factory.get("/lessons/")
        force_authenticate(request)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication(self) -> None:

        view = LessonListAPIView.as_view()
        request = self.factory.get("/lessons/")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"count": 0, "next": None, "previous": None, "results": []})
