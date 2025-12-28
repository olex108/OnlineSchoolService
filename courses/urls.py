from django.urls import path
from .apps import CoursesConfig
from rest_framework.routers import DefaultRouter

from . import views

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r"course", views.CourseViewSet, basename="course")


urlpatterns = [
    path("lesson/create/", views.LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lesson/", views.LessonListAPIView.as_view(), name="lesson-list"),
    path("lesson/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson-get"),
    path("lesson/<int:pk>/update/", views.LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lesson/<int:pk>/delete/", views.LessonDestroyAPIView.as_view(), name="lesson-delete"),
] + router.urls
