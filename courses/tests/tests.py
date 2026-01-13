from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, force_authenticate

from courses.models import Course
from courses.views import LessonListAPIView, CourseViewSet
from users.views import SubscribeAPIView
from users.models import User, Subscription

from django.urls import reverse


class AuthenticationTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='test_user@test.com', password='test_PASSWORD', is_active=True)

    def test_without_authentication(self):

        view = LessonListAPIView.as_view()
        request = self.factory.get('/lessons/')
        force_authenticate(request)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication(self):

        view = LessonListAPIView.as_view()
        request = self.factory.get('/lessons/')
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'count': 0, 'next': None, 'previous': None, 'results': []})


class SubscriptionTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_1 = User.objects.create(email='test_user_1@test.com', password='test_PASSWORD', is_active=True)
        # self.user_2 = User.objects.create(email='test_user_2@test.com', password='test_PASSWORD', is_active=True)
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Course',
            preview="",
            video_url="",
            owner=self.user_1,
        )
        self.subscription_1 = Subscription.objects.create(
            user=self.user_1,
            course=self.course,
            subscription=True,
        )
        # self.subscription_2 = Subscription.objects.create(
        #     user=self.user_2,
        #     course=self.course,
        #     subscription=False,
        # )

    def test_subscription(self):

        # Test subscription field of course
        course_view = CourseViewSet.as_view({"get": "retrieve"})
        course_retrieve_request = self.factory.get(reverse("courses:course-detail", kwargs={"pk": self.course.id}))
        force_authenticate(course_retrieve_request, user=self.user_1)
        course_retrieve_response = course_view(course_retrieve_request, pk=self.course.id)

        self.assertEqual(course_retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(course_retrieve_response.data['subscription'], True)

        # Test of post SubscribeAPIView
        subscription_view = SubscribeAPIView.as_view()
        subscription_request = self.factory.post(
            path=reverse("users:subscribe"),
            data={"course_id": self.course.id},
            format="json",
        )
        force_authenticate(subscription_request, user=self.user_1)
        subscription_response = subscription_view(subscription_request)

        self.assertEqual(subscription_response.status_code, status.HTTP_200_OK)
        self.assertEqual(subscription_response.data['message'], "Подписка удалена")

        # Test of change subscription field of course after SubscribeAPIView
        force_authenticate(course_retrieve_request, user=self.user_1)
        course_retrieve_response = course_view(course_retrieve_request, pk=self.course.id)

        self.assertEqual(course_retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(course_retrieve_response.data['subscription'], False)


class LessonTest(APITestCase):
    pass
