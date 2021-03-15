from django.contrib.auth.models import AbstractUser

# from django.contrib.postgres.fields import ArrayField
from django.db import models


class CustomUser(AbstractUser):
    points = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    badges = models.CharField(max_length=100, default="")
    completed_problems = models.CharField(
        max_length=200, default=""
    )  # e.g. 4Python10Math2Science
    challenge_streak = models.PositiveIntegerField(default=0)
    max_challenge_streak = models.PositiveIntegerField(default=0)
    friends = models.ManyToManyField("CustomUser", blank=True)


class FriendRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="receiver"
    )

    def __str__(self):
        return f"Sender: {self.user}, Receiver: {self.receiver}"