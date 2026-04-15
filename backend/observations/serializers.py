from rest_framework import serializers

from .models import Observation


class ObservationSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Observation
        fields = [
            "id",
            "user",
            "experiment",
            "type",
            "file",
            "file_url",
            "description",
            "geo_location",
            "created_at",
        ]
        read_only_fields = ["id", "user", "file_url", "created_at"]

    def get_file_url(self, obj: Observation):
        request = self.context.get("request")
        if not obj.file:
            return None
        if request is None:
            return obj.file.url
        return request.build_absolute_uri(obj.file.url)
