from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Interest


class CurrentCookieDefault(object):
    """ Because cookie_key is read_only in addition to being in a UniqueTogether-relationship,
        it introduces a special case that can be fixed as suggested by:
        https://stackoverflow.com/a/56061820
    """

    def set_context(self, serializer_field):
        self.cookie_key = serializer_field.context['request'].COOKIES.get('csrftoken')

    def __call__(self):
        return self.cookie_key


class InterestSerializer(serializers.ModelSerializer):
    cookie_key = serializers.CharField(read_only=True, default=CurrentCookieDefault())

    class Meta:
        model = Interest
        fields = ['id', 'cookie_key', 'group', 'created']
        validators = [
            UniqueTogetherValidator(
                queryset=Interest.objects.all(),
                fields=['cookie_key', 'group']
            )
        ]
