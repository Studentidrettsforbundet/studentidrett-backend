from django.db import models

from clubSports.models import ClubSport

# Create your models here.


class Interest(models.Model):
    email = models.EmailField()
    club_sport = models.ForeignKey(ClubSport, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['club_sport']
