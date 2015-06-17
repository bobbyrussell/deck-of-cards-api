import json

from rest_framework import serializers

import models


def encode_card(card):
    card_object = dict(card.__dict__)

    if 'code' in card_object.keys():
        del card_object['code']
    return card_object


class CardEncoder(json.JSONEncoder):

    def default(self, card):
        return encode_card(card)


def encode_pile(pile):
    piles = {}

    for name, named_pile in pile.piles.items():
        piles[name] = [encode_card(card) for card in named_pile]

    return piles


class PileEncoder(json.JSONEncoder):

    def default(self, pile):
        return encode_pile(pile)

def encode_deck(deck):
    fields = ['cards', 'pile', 'count']
    deck_object = deck.__dict__.items()
    encoded_deck = dict((k, v) for k, v in deck_object if k in fields)
    encoded_deck['cards'] = [encode_card(card) for card in deck.cards]
    encoded_deck['pile'] = encode_pile(deck.pile)

    if deck.deck_model:
        encoded_deck['id'] = deck.deck_model.id

    return encoded_deck


class DeckEncoder(json.JSONEncoder):

    def default(self, deck):
        return encode_deck(deck)


def decode_card(card):
    if 'suit' in card and 'rank' in card:
        return models.Card(suit=card['suit'], rank=card['rank'])


class CardDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=decode_card)


def decode_pile(pile):
    piles = {}

    for name, named_pile in pile.items():
        piles[name] = [decode_card(card) for card in named_pile]

    pile = models.Pile(piles=piles)
    return pile


class PileDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=decode_pile)


def decode_deck(deck):
    if 'cards' in deck and 'pile' in deck:
        cards = [decode_card(card) for card in deck['cards']]
        pile = decode_pile(deck['pile'])
        return models.Deck(cards=cards, pile=pile)
    else:
        raise Exception("Cannot Decode Deck!")


class DeckDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=decode_deck)
