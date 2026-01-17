from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate

from courses.models import Course
from courses.views import CourseViewSet, LessonListAPIView
from users.models import Subscription, User
from users.views import SubscribeAPIView


class SubscriptionTest(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

        self.user_1 = User.objects.create(email="test_user_1@test.com", password="test_PASSWORD", is_active=True)
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Course",
            preview="",
            video_url="",
            owner=self.user_1,
        )
        self.subscription_1 = Subscription.objects.create(
            user=self.user_1,
            course=self.course,
            subscription=True,
        )

    def test_subscription(self) -> None:

        # Test subscription field of course
        course_view = CourseViewSet.as_view({"get": "retrieve"})
        course_retrieve_request = self.factory.get(reverse("courses:course-detail", kwargs={"pk": self.course.id}))
        force_authenticate(course_retrieve_request, user=self.user_1)
        course_retrieve_response = course_view(course_retrieve_request, pk=self.course.id)

        self.assertEqual(course_retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(course_retrieve_response.data["subscription"], True)

        # Test of post SubscribeAPIView
        subscription_view = SubscribeAPIView.as_view()
        subscription_request = self.factory.get(
            path=reverse("users:subscribe", kwargs={"pk": self.course.id}),
        )

        force_authenticate(subscription_request, user=self.user_1)
        subscription_response = subscription_view(subscription_request, pk=self.course.id)

        self.assertEqual(subscription_response.status_code, status.HTTP_200_OK)
        self.assertEqual(subscription_response.data["message"], "Подписка удалена")

        # Test of change subscription field of course after SubscribeAPIView
        force_authenticate(course_retrieve_request, user=self.user_1)
        course_retrieve_response = course_view(course_retrieve_request, pk=self.course.id)

        self.assertEqual(course_retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(course_retrieve_response.data["subscription"], False)
