from rest_framework import serializers

from .models import Course, UserCourse


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "language", "type", "content_url", "thumbnail_url", "duration_minutes", "difficulty", "created_at"]
        read_only_fields = ["id", "created_at"]


class UserCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = UserCourse
        fields = ["id", "course", "completed", "progress", "created_at"]
        read_only_fields = ["id", "created_at"]
