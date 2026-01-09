from rest_framework import generics, viewsets
from users.permissions import IsModer
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .serializers import CourseRetrieveSerializer, CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseRetrieveSerializer
        else:
            return CourseSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [IsModer, IsAuthenticated]
        elif self.action == "update":
            self.permission_classes = [IsModer]
        elif self.action == "partial_update":
            self.permission_classes = [IsModer]
        elif self.action == "list":
            self.permission_classes = [IsModer, IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer, IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer, IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
