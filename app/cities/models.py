from django.db import models

from django.utils.translation import gettext_lazy as _
# Create your models here.

class Region(models.TextChoices):
    NORD = 'nord', _('Nord-Norge')
    MIDT = 'midt', _('Midt-Norge')
    VEST = 'vest', _('Vestlandet')
    SØR = 'sør', _('Sørlandet')
    ØST = 'øst', _('Østlandet')

class City(models.Model):

    name = models.CharField(max_length=31, null=False)
    region = models.CharField(max_length=4, null=False, choices=Region.choices)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['region']
