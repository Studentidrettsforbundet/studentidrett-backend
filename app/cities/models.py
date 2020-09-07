from django.db import models


# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=31, null=False)
    region = models.CharField(max_length=63, null=False)

    class Meta:
        ordering = ['region']
