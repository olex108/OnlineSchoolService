from rest_framework import serializers

from .models import Course, Lesson
from .validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ["name", "preview", "description", "video_url", "course"]
        validators = [VideoUrlValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ["name", "preview", "description", "video_url"]
        validators = [VideoUrlValidator(field="video_url")]


class CourseRetrieveSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set.all", many=True)

    def get_lessons_count(self, obj):
        return obj.lesson_set.all().count()

    class Meta:
        model = Course
        fields = "__all__"
