from django.db import models

# Create your models here.


class ObservationType(models.TextChoices):
    IMAGE = "image", "Image"
    AUDIO = "audio", "Audio"
    TEXT = "text", "Text"


class Observation(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="observations",
    )
    experiment = models.ForeignKey(
        "experiments.Experiment",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="observations",
    )
    type = models.CharField(max_length=10, choices=ObservationType.choices)
    file = models.FileField(upload_to="observations/", null=True, blank=True)
    description = models.TextField(blank=True, default="")
    geo_location = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.user.username}"
