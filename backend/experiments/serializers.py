from rest_framework import serializers

from experiments.models import Experiment


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ["id", "title", "description", "protocol", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]
