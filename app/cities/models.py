from django.db import models

from app.enums import Region

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True)
    region = models.CharField(max_length=4, null=False, choices=Region.choices)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["region"]
