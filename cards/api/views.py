from django.http import Http404

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import BadRequestException

from deck.encoders import encode_card
from deck.models import Deck, DeckModel, NotEnoughCardsException
from deck.serializers import DeckModelSerializer, HandSerializer
from deck.exceptions import NoSuchDeckException

class GetDeckMixIn(object):

    def get_deck(self, uuid):
        try:
            return Deck.get(uuid)
        except NoSuchDeckException:
            raise Http404


class DeckCreateAPIView(APIView):

    def post(self, request, format = None):
        count = request.query_params.get('count', 1)
        shuffle = request.query_params.get('shuffle', True)
        deck = DeckModel.create_deck(n=int(count), shuffle=shuffle)
        serialized_deck = DeckModelSerializer(deck.encode())
        return Response(serialized_deck.data, status=status.HTTP_201_CREATED)


class DeckDetailAPIView(GetDeckMixIn, APIView):

    def get(self, request, uuid, format = None):
        deck = self.get_deck(uuid)
        serialized_deck = DeckModelSerializer(deck.encode())
        return Response(serialized_deck.data)


class DeckDrawAPIView(GetDeckMixIn, APIView):

    def put(self, request, uuid, format = None):
        deck = self.get_deck(uuid)
        count = int(request.query_params.get('count', 1))

        try:
            if count == 1:
                cards = [encode_card(deck.draw())]
            else:
                cards = [encode_card(card) for card in deck.draw(count)]
        except NotEnoughCardsException:
            raise BadRequestException

        deck.save()
        serialized_hand = HandSerializer(data={"cards": cards})

        if serialized_hand.is_valid():
            return Response(serialized_hand.validated_data)
        else:
            raise Exception("Something Went Wrong")


class DeckShuffleAPIView(GetDeckMixIn, APIView):

    def put(self, request, uuid, format = None):
        deck = self.get_deck(uuid)
        deck.shuffle()
        deck.save()
        return Response()


class DeckDeleteAPIView(GetDeckMixIn, APIView):

    def delete(self, request, uuid, format = None):
        deck = self.get_deck(uuid)
        deck.delete()
        return Response()
