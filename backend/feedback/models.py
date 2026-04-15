from django.db import models

# Create your models here.


class Feedback(models.Model):
    observation = models.ForeignKey(
        "observations.Observation",
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )
    researcher = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="feedbacks_given",
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback #{self.id}"
