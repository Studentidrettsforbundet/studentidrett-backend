from django.db import models
from sports.models import Sport
from clubs.models import Club

# Create your models here.


class ClubSport(models.Model):
    name = models.CharField(max_length=30, blank=False, default='Sportsklubb')
    description = models.TextField(max_length=500, null=True)
    cover_photo = models.ImageField(upload_to='clubSports', null=True)
    sport_type = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    contact_email = models.EmailField(max_length=254, null=True)

    class Meta:
        ordering = ['name']
