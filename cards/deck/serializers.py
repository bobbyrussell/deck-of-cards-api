from rest_framework import serializers

from models import DeckModel, Card


class DeckModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeckModel
        fields = ('id', 'count', 'pile')
        read_only_fields = fields


class CardSerializer(serializers.Serializer):

    suit = serializers.CharField()
    rank = serializers.CharField()


class HandSerializer(serializers.Serializer):

    cards = CardSerializer(many=True)
