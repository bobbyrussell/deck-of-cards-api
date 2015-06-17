import collections
import json
import random
import uuid

from jsonfield import JSONField

from django.db import models

import encoders

from .exceptions import NotEnoughCardsException, NoSuchDeckException


class Card(object):

    SUITS = {
        "Hearts": "H", "Clubs": "C",
        "Diamonds": "D", "Spades": "S",
    }

    RANKS = {
        2: 1, 3: 2, 4: 3,
        5: 4, 6: 5, 7: 6,
        8: 7, 9: 8, 10: 9,
        "Jack": 10, "Queen": 11,
        "King": 12, "Ace": 13,
    }

    def __init__(self, rank, suit):
        try:
            self.rank = rank
            self.suit = suit
            self.code = (Card.SUITS[suit], Card.RANKS[rank])
        except KeyError as e:
            raise Exception("Invalid Card.")

    def __eq__(self, other):
        suit, rank = self.code

        if isinstance(other, int):
            try:
                other_rank = Card.RANKS[other]
            except KeyError:
                message = "Numerical operands must be between 2 and 10."
                raise Exception(message)

            if rank == other_rank:
                return True
            return False
        elif isinstance(other, str):
            try:
                other_rank = Card.RANKS[other]
            except KeyError:
                message = "Operands must be a valid Rank."
                raise Exception(message)

            if rank == other_rank:
                return True
            return False
        elif isinstance(other, Card):
            other_suit, other_rank = other.code

            if suit == other_suit and rank == other_rank:
                return True
            return False
        else:
            raise Exception("Operands must be Card or Int")

    def _calculate_rank(self, other):
        _, rank = self.code

        if isinstance(other, int):
            other_rank = Card.RANKS[other]
        elif isinstance(other, str):
            try:
                other_rank = Card.RANKS[other]
            except KeyError:
                raise Exception("Numerical card values must be between 2 and 10")
        elif isinstance(other, Card):
            _, other_rank = other.code
        else:
            raise Exception("Illegal Operation: Operands must be Card or Int")

        return rank, other_rank

    def __lt__(self, other):
        rank, other_rank = self._calculate_rank(other)

        if rank < other_rank:
            return True
        return False

    def __le__(self, other):
        return (self < other) or (self == other)

    def __gt__(self, other):
        return (not self < other) and (not self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck(object):

    @staticmethod
    def get(id):
        try:
            deck_model = DeckModel.objects.get(pk=id)
        except Exception:
            raise NoSuchDeckException("No Such Deck Exists")

        decoded_deck = deck_model.decode()
        decoded_deck.deck_model = deck_model
        return decoded_deck

    def __init__(self, n = 1, cards = None, pile = None,
                 deck_model = None, shuffle = True):
        self.pile = pile or Pile()
        self.deck_model = deck_model
        self.encoder = encoders.DeckEncoder()

        if cards:
            self.cards = cards
        else:
            self.cards = []

            suits, ranks = sorted(Card.SUITS.keys()), sorted(Card.RANKS.keys())
            for suit in suits:
                for rank in ranks:
                    for i in range(0, n):
                        self.cards.append(Card(rank, suit))

            if shuffle:
                self.shuffle()

        self.count = len(self.cards)

    @property
    def id(self):
        if self.deck_model:
            return str(self.deck_model.id)
        else:
            raise Exception("No ID set: Use DeckModel.create_deck() instead")

    def __iter__(self):
        return iter(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def _search(self, till):
        for i, card in enumerate(self):
            if card == till:
                return i
        return -1

    def draw(self, n = 1, till = None, from_pile = None):
        if from_pile:
            return self.pile.draw(n=n,from_pile=from_pile)

        if not self.has_cards() or n > self.count:
            raise NotEnoughCardsException("You're trying to draw more cards"
                                          " than are in the deck!")
        else:
            cards = []
            pool = self.cards[:]

            if till:
                index = self._search(till)
                if index >= 0:
                    pool, cards = pool[:index], pool[index:len(pool)]
                    cards.reverse()
                else:
                    cards, pool = pool, cards
            else:
                while n > 0:
                    cards.append(pool.pop())
                    n -= 1

            if len(cards) == 1:
                cards = cards[0]

            self.cards = pool
            self.count = len(self.cards)
            return cards

    def discard(self, card, into = None):
        self.pile.push(card, into=into)

    def has_cards(self):
        if self.count > 0:
            return True
        return False

    def encode(self):
        return self.encoder.default(self)

    def save(self):
        if self.deck_model:
            encoded_deck = self.encode()
            self.deck_model.cards = encoded_deck['cards']
            self.deck_model.pile  = encoded_deck['pile']
            self.deck_model.save()
        else:
            raise Exception("No Deck Model Set!")

    def delete(self):
        if self.deck_model:
            self.deck_model.delete()
        else:
            raise Exception("No Deck Model Set!")

    def __str__(self):
        string  = "Count: {}\n".format(self.count)
        string += "*" * len(string) + "\n"

        for i, card in enumerate(self.cards):
            string += "{}\t".format(i + 1) + str(card) + "\n"
        return string

    def __repr__(self):
        return "Deck ({} cards left)".format(self.count)


class DeckModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    count = models.IntegerField()
    cards = JSONField()
    pile  = JSONField()

    def __repr__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def decode(self):
        deck_object = {'cards': self.cards, 'pile': self.pile}
        return encoders.decode_deck(deck_object)

    @classmethod
    def create_deck(cls, *args, **kwargs):
        deck = Deck(*args, **kwargs)
        encoded_deck = deck.encode()
        deck.deck_model = cls.objects.create(
            cards=encoded_deck['cards'],
            pile=encoded_deck['pile'],
            count=encoded_deck['count']
        )
        return deck


class Pile(object):

    DEFAULT_PILE = "discard"

    def __init__(self, piles = None):
        self.piles = piles or {Pile.DEFAULT_PILE: []}

    def count(self, pile = None):
        if not pile:
            pile = Pile.DEFAULT_PILE
        the_pile = self.piles[pile]
        return len(the_pile)

    def push(self, card, into = None):
        try:
            pile = self.piles[into]
        except KeyError:
            if not into:
                pile = self.piles[Pile.DEFAULT_PILE]
            else:
                self.piles[into] = pile = []

        if isinstance(card, Card):
            pile.append(card)
        elif isinstance(card, list):
            if all([isinstance(c, Card) for c in card]):
                for c in card:
                    pile.append(c)
        else:
            raise Exception("You may only discard a Card or a list of Cards")

    def draw(self, n = 1, from_pile = None):
        from_pile = from_pile or Pile.DEFAULT_PILE

        try:
            pile = self.piles[from_pile]
        except KeyError:
            raise Exception("You cannot draw from a pile that does not exist.")

        pile_count = len(pile)

        if not (pile_count > 0) or (n > pile_count):
            raise NotEnoughCardsException("You're trying to draw more cards"
                                          " than are in the deck!")
        else:
            cards = []
            pool = pile[:]

            while n > 0:
                cards.append(pool.pop())
                n -= 1

            return cards

    def show(self, pile = None):
        return self.piles.get(pile, self.piles[Pile.DEFAULT_PILE])

    def __repr__(self):
        return 'Pile with ' + str(self.piles)

    def __str__(self):
        return 'Pile with ' + str(self.piles)

    def __str__(self):
        string  = "Piles:\n"
        string += "*" * len(string) + "\n"

        for key, cards in self.piles.items():
            string += "'" + key + "'\n"
            if not cards:
                string += "\t* (Nothing here)\n"
            else:
                for card in cards:
                    string += "\t* " + str(card) + "\n"
        return string
