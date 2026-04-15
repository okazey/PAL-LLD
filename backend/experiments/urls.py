from django.urls import include, path
from rest_framework.routers import DefaultRouter

from experiments.views import ExperimentViewSet

router = DefaultRouter()
router.register(r"", ExperimentViewSet, basename="experiments")

urlpatterns = [
    path("", include(router.urls)),
]
