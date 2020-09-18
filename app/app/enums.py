from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.TextChoices):
    NORD = 'nord', _('Nord-Norge')
    MIDT = 'midt', _('Midt-Norge')
    VEST = 'vest', _('Vestlandet')
    SØR = 'sør', _('Sørlandet')
    ØST = 'øst', _('Østlandet')