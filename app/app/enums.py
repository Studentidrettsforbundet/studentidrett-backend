from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.TextChoices):
    NORD = 'nord', _('Nord-Norge')
    MIDT = 'midt', _('Midt-Norge')
    VEST = 'vest', _('Vestlandet')
    SOR = 'sør', _('Sørlandet')
    OST = 'øst', _('Østlandet')