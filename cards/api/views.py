from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from deck.models import Deck, DeckModel
from deck.serializers import DeckModelSerializer


class DeckCreateAPIView(APIView):

    def post(self, request, format = None):
        deck = DeckModel.create_deck()
        serialized_deck = DeckModelSerializer(deck.encode())
        return Response(serialized_deck.data, status=status.HTTP_201_CREATED)


class DeckDetailAPIView(APIView):

    def get_object(self, uuid):
        try:
            return Deck.get(uuid)
        except DeckModel.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format = None):
        deck = self.get_object(uuid)
        serialized_deck = DeckModelSerializer(deck.encode())
        return Response(serialized_deck.data)
