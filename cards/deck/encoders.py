import json

import deck.models

class CardEncoder(json.JSONEncoder):

    def default(self, card):
        encoded_card = dict((k, v) for k, v in card.__dict__.items())
        return card.__dict__


class DeckEncoder(json.JSONEncoder):

    def default(self, _deck):
        encoder = CardEncoder()
        cards = [encoder.encode(card) for card in _deck.cards]
        encoded_deck = dict((k, v) for k, v in _deck.__dict__.items())
        encoded_deck['cards'] = cards

        if isinstance(_deck.pile, deck.models.Deck):
            pile_cards = self.default(_deck.pile)
            encoded_deck['pile'] = pile_cards

        return encoded_deck


def card_decoder(card):
    if 'suit' in card and 'rank' in card:
        return deck.models.Card(suit=card['suit'], rank=card['rank'])


class CardDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=card_decoder)


def deck_decoder(_deck):
    if 'count' in _deck and 'cards' in _deck:
        card_decoder = CardDecoder()
        cards = [card_decoder.decode(card) for card in _deck['cards']]

        if not _deck['pile']:
            pile = deck.models.Deck(0)
        else:
            pile = deck_decoder(_deck['pile'])
        return deck.models.Deck(cards=cards, pile=pile)
    else:
        raise Exception("Cannot Decode Deck!")


class DeckDecoder(object):

    def decode(self, obj):
        return json.loads(obj, object_hook=deck_decoder)
