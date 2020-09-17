from django.db import models
from sports.models import Sport
from clubs.models import Club
from cities.models import City

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=30, blank=False, default='Group')
    description = models.TextField(max_length=500, null=True)
    cover_photo = models.ImageField(upload_to='groups', null=True)
    sport_type = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, related_name="groups") #TODO on_delete=models.CASCADE,
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="groups")#TODO on_delete=models.CASCADE,
    #contact_person = models.CharField(max_length=30, blank=True, default='', null=True)
    #contact_email = models.EmailField(max_length=254, null=True)

    class Meta:
        ordering = ['name']
