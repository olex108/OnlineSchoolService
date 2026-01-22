from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from users.models import Subscription
from users.permissions import IsModer, IsOwner

from .models import Course, Lesson
from .paginators import CustomCoursesPaginator
from .serializers import CourseRetrieveSerializer, CourseSerializer, LessonSerializer

from .tasks import mailing_to_course_subscribers


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomCoursesPaginator

    def perform_create(self, serializer: CourseSerializer) -> None:
        serializer.save(owner=self.request.user)

    def get_serializer_class(self) -> serializers:
        if self.action == "retrieve":
            return CourseRetrieveSerializer
        else:
            return CourseSerializer

    def get_permissions(self) -> list:
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "update":
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == "partial_update":
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer: CourseSerializer) -> None:
        course = serializer.save()
        mailing_to_course_subscribers.delay(course.pk)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Create a new lesson. For authenticated users
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer: LessonSerializer) -> None:
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    Get List of lessons by page param.  For authenticated users
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomCoursesPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Get Lesson by lesson id.  For authenticated users
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Update Lesson by lesson id.  For lesson owner or moderator users
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Delete Lesson by lesson id.  For owner user
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
