from django.db import models


class Questionnaire(models.Model):
    qna = models.CharField(max_length=10)  # TODO: edit qna field to accept a list of tuples
