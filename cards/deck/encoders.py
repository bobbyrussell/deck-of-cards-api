import json

from rest_framework import serializers

import models


class CardEncoder(json.JSONEncoder):

    def default(self, card):
        return dict((k, v) for k, v in card.__dict__.items())


class DeckEncoder(json.JSONEncoder):

    def default(self, deck):
        fields = ['cards', 'pile', 'count']
        cards = [CardEncoder().encode(card) for card in deck.cards]
        deck_object = deck.__dict__.items()
        encoded_deck = dict((k, v) for k, v in deck_object if k in fields)
        encoded_deck['cards'] = cards

        if isinstance(deck.pile, models.Deck):
            pile_cards = self.default(deck.pile)
            encoded_deck['pile'] = pile_cards

            if deck.deck_model:
                encoded_deck['id'] = deck.deck_model.id

        return encoded_deck


def card_decoder(card):
    if 'suit' in card and 'rank' in card:
        return models.Card(suit=card['suit'], rank=card['rank'])


class CardDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=card_decoder)


def deck_decoder(_deck):
    if 'count' in _deck and 'cards' in _deck:
        cards = [CardDecoder().decode(card) for card in _deck['cards']]

        if not _deck['pile']:
            pile = models.Deck(0)
        else:
            pile = deck_decoder(_deck['pile'])
        return models.Deck(cards=cards, pile=pile)
    else:
        raise Exception("Cannot Decode Deck!")


class DeckDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=deck_decoder)
