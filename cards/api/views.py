from django.http import Http404

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import BadRequestException

from deck.encoders import encode_card, decode_card
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
        try:
            count = int(request.query_params.get('count', 1))
        except ValueError:
            raise BadRequestException(detail="Count Must be of type Int")

        shuffle_flag = request.query_params.get('shuffle', "true").lower()

        if shuffle_flag == "true":
            shuffle = True
        elif shuffle_flag == "false":
            shuffle = False
        else:
            raise BadRequestException(detail="Shuffle must be True or False.")

        deck = DeckModel.create_deck(n=count, shuffle=shuffle)
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


class DeckDiscardAPIView(GetDeckMixIn, APIView):

    def put(self, request, uuid, format = None):
        deck = self.get_deck(uuid)
        cards = request.data

        if not cards:
            raise BadRequestException(detail="You must PUT data.")
        else:
            try:
                decoded_cards = [decode_card(card) for card in cards]
            except:
                format_example = '[ {"rank": 2 ,"suit": "Diamonds"}, ... ]'
                message = ("Cannot decode cards. "
                           "The card format is:\n{}".format(format_example))
                raise BadRequestException(detail=message)
            into = request.query_params.get('into')
            try:
                deck.discard(decoded_cards, into=into)
            except:
                message = ("Invalid pile name. Make sure into param is a"
                           " hashable type")
                raise BadRequestException(detail=message)
            deck.save()
        return Response()
