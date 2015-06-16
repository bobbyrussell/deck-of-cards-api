import json

from rest_framework import serializers

import models


class CardEncoder(json.JSONEncoder):

    def default(self, card):
        card_object = dict(card.__dict__)

        if 'code' in card_object.keys():
            del card_object['code']
        return card_object


class PileEncoder(json.JSONEncoder):

    def default(self, pile):
        piles = dict(pile.piles)

        for name, pile in pile.piles.items():
            piles[name] = [CardEncoder().encode(card) for card in pile]

        return piles


class DeckEncoder(json.JSONEncoder):

    def default(self, deck):
        fields = ['cards', 'pile', 'count']
        deck_object = deck.__dict__.items()
        encoded_deck = dict((k, v) for k, v in deck_object if k in fields)
        encoder = CardEncoder()
        encoded_deck['cards'] = [encoder.encode(card) for card in deck.cards]
        encoded_deck['pile'] = PileEncoder().encode(deck.pile)

        if deck.deck_model:
            encoded_deck['id'] = deck.deck_model.id

        return encoded_deck


def card_decoder(card):
    if 'suit' in card and 'rank' in card:
        return models.Card(suit=card['suit'], rank=card['rank'])


class CardDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=card_decoder)


def pile_decoder(pile):
    if not isinstance(pile, dict):
        try:
            pile = json.loads(pile)
        except:
            raise Exception("Piles should be dict or JSON objects")

    piles = dict(pile)

    for name, pile in pile.items():
        piles[name] = [CardDecoder().decode(card) for card in pile]

    return models.Pile(piles=piles)


class PileDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=pile_decoder)


def deck_decoder(deck):
    if 'cards' in deck and 'pile' in deck:
        cards = [CardDecoder().decode(card) for card in deck['cards']]
        pile = pile_decoder(deck['pile'])
        deck = models.Deck(cards=cards, pile=pile)
        return deck
    else:
        raise Exception("Cannot Decode Deck!")


class DeckDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=deck_decoder)
