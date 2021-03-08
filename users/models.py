from django.contrib.auth.models import AbstractUser

# from django.contrib.postgres.fields import ArrayField
from django.db import models


class Customuser(AbstractUser):
    points = models.PositiveIntegerField()
    streak = models.PositiveIntegerField()
    longest_streak = models.PositiveIntegerField()
    answered = models.JSONField()
    # badges = ArrayField(models.PositiveIntegerField(), size=)
