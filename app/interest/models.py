from django.db import models

from groups.models import Group

# Create your models here.


class Interest(models.Model):
    email = models.EmailField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['group']
