from django.db import models
from groups.models import Group
# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=63)
    full_capacity = models.BooleanField()
    tryouts = models.BooleanField()
    registration_open = models.BooleanField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

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
