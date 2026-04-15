from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from observations.models import Observation
from observations.serializers import ObservationSerializer


class ObservationViewSet(viewsets.ModelViewSet):
    serializer_class = ObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = Observation.objects.select_related("user", "experiment").order_by("-created_at")
        user = self.request.user

        role = getattr(user, "role", "")
        if role == "FARMER":
            return qs.filter(user=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
