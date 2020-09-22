from django.db import models

from cities.models import City


# Create your models here.


class Club(models.Model):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="clubs")
    name = models.CharField(max_length=255, null=False)
    Description = models.CharField(max_length=1023, null=True)
    contact_email = models.EmailField(max_length=127, null=True)
    pricing = models.CharField(max_length=255, null=True)
    register_info = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
