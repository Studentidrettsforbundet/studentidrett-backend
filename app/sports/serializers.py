from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from sports.models import Sport


class SportSerializer(serializers.ModelSerializer):
    """name = serializers.CharField(
        validators=[UniqueValidator(queryset=Sport.objects.all())]
    )"""

    class Meta:
        model = Sport
        fields = ["id", "name"]
