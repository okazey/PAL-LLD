from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course, UserCourse
from .serializers import CourseSerializer, UserCourseSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Course.objects.order_by("-created_at")

    @action(detail=False, methods=["get"], url_path="my-courses")
    def my_courses(self, request):
        user_courses = UserCourse.objects.filter(
            user=request.user
        ).select_related("course").order_by("-created_at")
        serializer = UserCourseSerializer(user_courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        course = self.get_object()
        user_course, created = UserCourse.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={"completed": True},
        )
        if not created and not user_course.completed:
            user_course.completed = True
            user_course.save(update_fields=["completed"])

        serializer = UserCourseSerializer(user_course)
        return Response(serializer.data, status=status.HTTP_200_OK)
