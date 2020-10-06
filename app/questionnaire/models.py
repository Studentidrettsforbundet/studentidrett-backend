from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=50)
    left = models.CharField(max_length=20)
    right = models.CharField(max_length=20)


class Answer(models.Model):
    qid = models.CharField(max_length=4)
    answer = models.IntegerField()
