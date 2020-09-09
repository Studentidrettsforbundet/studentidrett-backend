from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=63)
    full_capacity = models.BooleanField()
    tryouts = models.BooleanField()
    registration_open = models.BooleanField()
    club_sport = models.IntegerField()
    #club_sport = models.ForeignKey(ClubSport, on_delete=models.CASCADE) temporary removed before ClubSports is made

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
