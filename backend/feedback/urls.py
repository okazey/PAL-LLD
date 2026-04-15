from django.urls import path

from .views import FeedbackByObservationView, FeedbackCreateView

urlpatterns = [
    path("", FeedbackCreateView.as_view(), name="feedback-create"),
    path("<int:observation_id>/", FeedbackByObservationView.as_view(), name="feedback-by-observation"),
]
