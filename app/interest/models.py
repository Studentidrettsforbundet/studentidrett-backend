from django.db import models

from clubs.models import Club

# Create your models here.

# TODO: set sport as ForeignKey


class Interest(models.Model):
    email = models.EmailField()
    sport = models.CharField(max_length=127)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['sport']
