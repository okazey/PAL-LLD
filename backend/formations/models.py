from django.db import models


class CourseLanguage(models.TextChoices):
    FR = "FR", "Français"
    WOLOF = "WOLOF", "Wolof"


class CourseType(models.TextChoices):
    AUDIO = "audio", "Audio"
    VIDEO = "video", "Vidéo"


class CourseDifficulty(models.TextChoices):
    BEGINNER = "beginner", "Débutant"
    INTERMEDIATE = "intermediate", "Intermédiaire"
    ADVANCED = "advanced", "Avancé"


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    language = models.CharField(max_length=10, choices=CourseLanguage.choices, default=CourseLanguage.FR)
    type = models.CharField(max_length=10, choices=CourseType.choices, default=CourseType.AUDIO)
    content_url = models.URLField()
    thumbnail_url = models.URLField(blank=True, default="")
    duration_minutes = models.PositiveSmallIntegerField(default=0, help_text="Durée estimée en minutes")
    difficulty = models.CharField(max_length=20, choices=CourseDifficulty.choices, default=CourseDifficulty.BEGINNER)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_courses",
    )
    course = models.ForeignKey(
        "formations.Course",
        on_delete=models.CASCADE,
        related_name="user_courses",
    )
    completed = models.BooleanField(default=False)
    progress = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="unique_user_course")
        ]

    def __str__(self):
        return f"{self.user.username} – {self.course.title}"
