from django.db import models

# Create your models here.


class Experiment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    protocol = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiments_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Participation(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="participations",
    )
    experiment = models.ForeignKey(
        "experiments.Experiment",
        on_delete=models.CASCADE,
        related_name="participations",
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "experiment"], name="unique_participation")
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.experiment.title}"
