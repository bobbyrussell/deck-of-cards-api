import random

from django.db import models

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
            other_rank = other
            if rank == other_rank:
                return True
            return False
        elif isinstance(other, Card):
            other_suit, other_rank = other.code
            if suit == other_suit and rank == other_rank:
                return True
            return False
        else:
            raise Exception("Illegal Operation: Operand must be Card or Int")

    def __lt__(self, other):
        _, rank = self.code
        if isinstance(other, int):
            other_rank = other
        elif isinstance(other, Card):
            _, other_rank = other.code
        else:
            raise Exception("Illegal Operation: Operand must be Card or Int")

        if rank < other_rank:
            return True
        return False

    def __gt__(self, other):
        return not (self < other)

    def __le__(self, other):
        if isinstance(other, int):
            return (self < other) or (self == other)
        else:
            raise Exception("Illegal Operation: Operand must be Card or Int")

    def is_black(self):
        if self.suit in ["Spades", "Clubs"]:
            return True
        return False

    def is_red(self):
        return not self.is_black()

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck(object):

    def __init__(self, n = 1):
        self.cards = []
        self.pile = None
        for suit in Card.SUITS.keys():
            for rank in Card.RANKS.keys():
                for i in range(0, n):
                    self.cards.append(Card(rank, suit))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    @property
    def count(self):
        return len(self.cards)

    def draw(self, n = 1, till = None):
        if not self.has_cards() or n > self.count:
            raise Exception("You're trying to draw more cards than are in the"
                            " deck")
        else:
            cards = []
            pool = self.cards[:]
            while n > 0:
                card = pool.pop()
                cards.append(card)
                if till and card == till:
                    break
                n -= 1
            if len(cards) == 1:
                cards = cards[0]
            self.cards = pool
            return cards

    def discard(self, card):
        if not self.pile:
            self.pile = Deck(0)
        self.pile.cards.append(card)

    def has_cards(self):
        if self.count > 0:
            return True
        return False

    def __str__(self):
        string = "Count: {}\n".format(self.count)
        string += "*" * len(string) + "\n"
        for i, card in enumerate(self.cards):
            string += "{}\t".format(i + 1) + str(card) + "\n"
        return string
