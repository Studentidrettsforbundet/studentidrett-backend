from django.db import models

from cities.models import City
from clubs.models import Club
from sports.models import Sport

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, default="Group")
    description = models.TextField(max_length=500, null=True)
    cover_photo = models.ImageField(upload_to="groups", null=True)
    sports = models.ManyToManyField(Sport)
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, null=True, related_name="groups"
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, related_name="groups"
    )
    contact_email = models.EmailField(max_length=40, null=True)

    class Meta:
        ordering = ["name"]
