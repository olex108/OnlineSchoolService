from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from courses.views import (
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)
from users.models import User


class LessonTest(APITestCase):
    fixtures = [
        "test_users_fixtures.json",
        "test_courses_fixtures.json",
        "test_lessons_fixtures.json",
        "test_payment_fixtures.json",
        "test_group_fixtures.json",
    ]

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

        # Get users
        self.owner = User.objects.get(email="user_owner@test.com")
        self.user = User.objects.get(email="user@test.com")
        self.moderator = User.objects.get(email="user_moderator@test.com")
        self.moderator_group = Group.objects.get(name="Модераторы")
        # Add user "user_moderator@test.com" to group "Модераторы"
        self.moderator.groups.add(self.moderator_group)

        # create views and requests
        # list
        self.list_view = LessonListAPIView.as_view()
        self.list_request = self.factory.get(
            path=reverse("courses:lesson-list"),
        )
        # retrieve
        self.retrieve_view = LessonRetrieveAPIView.as_view()
        self.retrieve_request = self.factory.get(reverse("courses:course-detail", kwargs={"pk": 1}))
        # create
        self.crate_view = LessonCreateAPIView.as_view()
        self.create_request = self.factory.post(
            path=reverse("courses:lesson-create"),
            data={
                "name": "New Lesson",
                "preview": None,
                "description": "New description",
                "video_url": "",
                "course": 1,
            },
            format="json",
        )
        # update
        self.update_view = LessonUpdateAPIView.as_view()
        self.update_request = self.factory.put(
            path=reverse("courses:lesson-update", kwargs={"pk": 1}),
            data={
                "name": "Update Lesson",
                "preview": None,
                "description": "Update description",
                "video_url": "",
                "course": 1,
            },
            format="json",
        )
        # destroy
        self.destroy_view = LessonDestroyAPIView.as_view()
        self.destroy_request = self.factory.delete(
            path=reverse("courses:lesson-delete", kwargs={"pk": 1}),
        )

    def test_lesson_list(self) -> None:

        force_authenticate(self.list_request, user=self.owner)
        list_response = self.list_view(self.list_request)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 2)

    def test_lesson_retrieve(self) -> None:

        force_authenticate(self.retrieve_request, user=self.owner)
        retrieve_response = self.retrieve_view(self.retrieve_request, pk=1)

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data["name"], "Test_1")

    def test_lesson_create(self) -> None:

        force_authenticate(self.create_request, user=self.owner)
        create_response = self.crate_view(self.create_request)

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["name"], "New Lesson")

        force_authenticate(self.list_request, user=self.owner)
        list_response = self.list_view(self.list_request)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 3)

    def test_lesson_create_moderator(self) -> None:

        force_authenticate(self.create_request, user=self.moderator)
        create_response = self.crate_view(self.create_request)
        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_owner(self) -> None:
        force_authenticate(self.update_request, user=self.owner)
        update_response = self.update_view(self.update_request, pk=1)

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["name"], "Update Lesson")
#
    def test_lesson_update_moderator(self) -> None:
        force_authenticate(self.update_request, user=self.moderator)
        update_response = self.update_view(self.update_request, pk=1)

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["name"], "Update Lesson")

    def test_lesson_update_user(self) -> None:
        force_authenticate(self.update_request, user=self.user)
        update_response = self.update_view(self.update_request, pk=1)
        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_destroy_owner(self) -> None:

        force_authenticate(self.destroy_request, user=self.owner)
        destroy_response = self.destroy_view(self.destroy_request, pk=1)

        self.assertEqual(destroy_response.status_code, status.HTTP_204_NO_CONTENT)

        force_authenticate(self.list_request, user=self.owner)
        list_response = self.list_view(self.list_request)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 1)

    def test_lesson_destroy_moderator(self) -> None:

        force_authenticate(self.destroy_request, user=self.moderator)
        destroy_response = self.destroy_view(self.destroy_request, pk=1)
        self.assertEqual(destroy_response.status_code, status.HTTP_403_FORBIDDEN)
