from rest_framework import generics, permissions

from feedback.models import Feedback
from feedback.permissions import IsResearcher
from feedback.serializers import FeedbackSerializer
from observations.models import Observation


class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsResearcher]

    def perform_create(self, serializer):
        serializer.save(researcher=self.request.user)


class FeedbackByObservationView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        observation_id = self.kwargs["observation_id"]
        qs = Feedback.objects.filter(observation_id=observation_id).select_related(
            "researcher", "observation"
        )

        user = self.request.user
        role = getattr(user, "role", "")

        if role == "FARMER":
            obs = Observation.objects.filter(id=observation_id, user=user).first()
            if obs is None:
                return Feedback.objects.none()

        return qs.order_by("created_at")
