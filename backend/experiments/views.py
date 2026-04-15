from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from experiments.models import Experiment, Participation
from experiments.permissions import IsFarmer, IsResearcher
from experiments.serializers import ExperimentSerializer


class ExperimentViewSet(viewsets.ModelViewSet):
    serializer_class = ExperimentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return Experiment.objects.select_related("created_by").order_by("-created_at")

    def create(self, request, *args, **kwargs):
        if not IsResearcher().has_permission(request, self):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="join")
    def join(self, request, pk=None):
        if not IsFarmer().has_permission(request, self):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        experiment = self.get_object()
        Participation.objects.get_or_create(user=request.user, experiment=experiment)
        return Response({"detail": "joined"}, status=status.HTTP_200_OK)
