from django.db import models
from clubSports.models import ClubSport
from sports.models import Sport
# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=63)
    club_sport = models.ForeignKey(ClubSport, on_delete=models.CASCADE, null=False)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=False)
    location = models.CharField(max_length=63)
    description = models.CharField(max_length=1023)

    class Meta:
        """ Configure the name displayed in the admin panel """
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name

    def get_full_capacity(self):
        return self.full_capacity

    def get_tryouts(self):
        return self.tryouts

    def get_registration_open(self):
        return self.registration_open
