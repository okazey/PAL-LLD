from rest_framework import serializers

from feedback.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "observation", "researcher", "comment", "created_at"]
        read_only_fields = ["id", "researcher", "created_at"]
