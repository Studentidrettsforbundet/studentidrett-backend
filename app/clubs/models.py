from django.db import models
from pygments import highlight


class Club(models.Model):
    name = models.CharField(max_length=100, default='')
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=11, blank = True)
    pricing = models.FloatField(null=True)
    register_info = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User', related_name='clubs', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

