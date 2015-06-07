import json

from .models import Card, Deck


class CardEncoder(json.JSONEncoder):

    def default(self, obj):
        return obj.__dict__


class DeckEncoder(json.JSONEncoder):

    def default(self, deck):
        encoder = CardEncoder()
        cards = [encoder.encode(card) for card in deck.cards]
        encoded_deck = dict((k, v) for k, v in deck.__dict__.items())
        encoded_deck['cards'] = cards
        return encoded_deck


def card_decoder(card):
    if 'suit' in card and 'rank' in card:
        return Card(suit=card['suit'], rank=card['rank'])


class CardDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=card_decoder)


def deck_decoder(deck):
    if 'count' in deck and 'cards':
        card_decoder = CardDecoder()
        cards = [card_decoder.decode(card) for card in deck['cards']]

        if not deck['pile']:
            pile = Deck(0)
        else:
            pile = deck_decoder(deck['pile'])
        return Deck(cards=cards, pile=pile)
    else:
        raise Exception("Cannot Decode Deck!")


class DeckDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=deck_decoder)
