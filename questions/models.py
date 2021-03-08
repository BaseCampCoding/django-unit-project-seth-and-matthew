from django.db import models

# from django.contrib.postgres.fields import ArrayField
class Question(models.Model):
    # possible_answers = ArrayField(models.CharField(max_length=120, size=4))
    category = models.CharField(max_length=30)
    correct_answer = models.CharField(max_length=120)
    description = models.TextField()