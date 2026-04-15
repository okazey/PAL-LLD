from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserRole(models.TextChoices):
    FARMER = "FARMER", "Farmer"
    RESEARCHER = "RESEARCHER", "Researcher"
    ADMIN = "ADMIN", "Admin"
    CONTENT_CREATOR = "CONTENT_CREATOR", "Content Creator"

class User(AbstractUser):
    role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.FARMER)
    phone = models.CharField(max_length=50, blank=True, default="")
    language = models.CharField(max_length=20, blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
