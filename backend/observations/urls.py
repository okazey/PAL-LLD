from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ObservationViewSet

router = DefaultRouter()
router.register(r"", ObservationViewSet, basename="observations")

urlpatterns = [
    path("", include(router.urls)),
]
