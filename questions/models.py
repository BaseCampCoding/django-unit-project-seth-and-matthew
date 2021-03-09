from django.db import models
from django.urls import reverse
# from django.contrib.postgres.fields import ArrayField
class Question(models.Model):
    category = models.CharField(max_length=30)
    correct_answer = models.PositiveIntegerField(default=1)
    description = models.TextField()
    possible_answers = [1,2,3,4]
    # def get_absolute_url(self):
    #     return reverse("home")