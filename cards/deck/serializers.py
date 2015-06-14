from rest_framework import serializers

from models import DeckModel


class DeckModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeckModel
        fields = ('id', 'count', 'pile')
        read_only_fields = ('id', 'count', 'pile')
