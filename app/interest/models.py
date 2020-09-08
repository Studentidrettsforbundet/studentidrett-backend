from django.db import models

# Create your models here.

# TODO: set sport as ForeignKey


class Interest(models.Model):
    email = models.EmailField()
    sport = models.CharField(max_length=127)
    club = models.CharField(max_length=63)

    class Meta:
        ordering = ['sport']
