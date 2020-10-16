from django.db import models

from app.enums import Gender, Skill, Status
from cities.models import City
from groups.models import Group
from sports.models import Sport

from django.utils import timezone

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=50, null=False)
    location = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    long_description = models.CharField(max_length=255, null=True)
    short_description = models.CharField(max_length=30, null=True)
    cost = models.CharField(max_length=511, null=True)
    equipment = models.CharField(max_length=511, null=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.ANY)
    skill_level = models.CharField(
        max_length=4, choices=Skill.choices, default=Skill.NONE
    )
    season = models.CharField(max_length=511, null=True)
    facebook_link = models.CharField(max_length=127, null=True)
    instagram_link = models.CharField(max_length=127, null=True)
    webpage = models.CharField(max_length=127, null=True)
    availability = models.CharField(
        max_length=2, choices=Status.choices, default=Status.FULL
    )
    image = models.ImageField(upload_to="teams", null=True)

    class Meta:
        """ Configure the name displayed in the admin panel """

        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name


class Schedule(models.Model):
    date = models.DateTimeField(default=timezone.now)
    team = models.ManyToManyField(Team, related_name="schedule")


class TryoutDates(models.Model):
    date = models.DateTimeField(default=timezone.now)
    team = models.ManyToManyField(Team, related_name="tryout_dates")
