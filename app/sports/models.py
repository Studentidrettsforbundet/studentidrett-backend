from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)

    class Meta:
        ordering = ["name"]
