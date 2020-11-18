from django.db import models

from sports.models import Sport


class Question(models.Model):
    text = models.CharField(max_length=100)

    class Meta:
        ordering = ["id"]


class Answer(models.Model):
    qid = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.SmallIntegerField()


class Alternative(models.Model):
    qid = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="alternatives"
    )
    text = models.CharField(max_length=20)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ["qid", "text"]


class Label(models.Model):
    text = models.CharField(max_length=25)
    sports = models.ManyToManyField(Sport, related_name="labels")
    alternatives = models.ManyToManyField(Alternative, related_name="labels")
