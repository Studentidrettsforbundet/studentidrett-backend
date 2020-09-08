from django.db import models

# Create your models here.

# TODO: set sport as ForeignKey


class Interest(models.Model):
    email = models.EmailField()
    sport = models.CharField(max_length=127)

    class Meta:
        ordering = ['sport']
