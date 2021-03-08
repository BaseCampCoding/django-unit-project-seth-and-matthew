from django.contrib.auth.models import AbstractUser

# from django.contrib.postgres.fields import ArrayField
from django.db import models


class CustomUser(AbstractUser):
    points = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    # badges = ArrayField(models.PositiveIntegerField(), size=)
