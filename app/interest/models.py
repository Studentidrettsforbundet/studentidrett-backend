from django.db import models

from groups.models import Group


class Interest(models.Model):
    session_id = models.CharField(max_length=100, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["group"]
        constraints = [
            models.UniqueConstraint(
                fields=["session_id", "group"], name="unique_interest"
            )
        ]
