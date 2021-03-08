from django.db import models

# from django.contrib.postgres.fields import ArrayField
class Question(models.Model):
    category = models.CharField(max_length=30)
    correct_answer = models.PositiveIntegerField(default=1)
    description = models.TextField()