"""
.. module:: deck.models
   :synopsis: Contains the implementation of a deck of cards.

.. moduleauthor:: Bobby Russell <bobbyrussell@gmail.com>

"""

import collections
import json
import random
import uuid

from jsonfield import JSONField

from django.db import models

import encoders

from .exceptions import NotEnoughCardsException, NoSuchDeckException


class Card(object):
    """Card: Playing Card Object

    A simple playing card. Each card has a suit and a rank. Options for a suit
    are the strings Hearts, Clubs, Diamonds, or Spades. Options for a rank are
    the numbers 2 through 10, or the strings Jack, Queen, King, or Ace.

    Card implements comparison using the dunder methods :func:__eq__ and
    :func:__lt__ against encoded ranks.
    """

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
        """Initialize a Card: Card(rank, suit)

        Args:
            rank (int or str): The cards rank
            suit (str): The cards suit

        Attributes:
            rank (int or str): The cards rank
            suit (str): The cards suit

        Raises:
            Exception if invalid suits or ranks are passed
        """
        try:
            self.rank = rank
            self.suit = suit
            self.code = (self.SUITS[suit], self.RANKS[rank])
        except KeyError as e:
            raise Exception("Invalid Card.")

    def __eq__(self, other):
        """Determine if a card is equal to a given value

        Args:
            other (int or str or |card|): Value or reference to compare against

        Raises:
            Exception if the :param other: is invalid.

        Returns:
            bool: True if |self| and :param other: other are equal, and False
            otherwise

        Compare the rank value of a :type str: or :type int: against
        |self|'s rank. If :param other: is a |card|, both suit and rank must be
        equal.
        """
        suit, rank = self.code
        try:
            other_rank = self.RANKS[other]

            if rank == other_rank:
                return True
            return False
        except KeyError:
            try:
                other_suit, other_rank = other.code

                if suit == other_suit and rank == other_rank:
                    return True
                return False
            except AttributeError:
                raise Exception

    def __ne__(self, other):
        return not self == other

    def _calculate_rank(self, other):
        """Translate the rank of another card or rank value into an encoded rank

        Args:
            other (int or str or Card): a rank or Card

        Raises:
            Exception if the :param other: is invalid.

        Returns:
            tuple: The encoded ranks of both self and other, respectively

        Generate a tuple with the encoded ranks of both |self| and the
        :param other:. This rank is used internally to make comparisons easier
        to implement.
        """
        _, rank = self.code

        try:
            other_rank = Card.RANKS[other]
        except KeyError:
            try:
                _, other_rank = other.code
            except AttributeError:
                raise Exception

        return rank, other_rank

    def __lt__(self, other):
        """Determine if a card is less than a given value

        Args:
            other (int or str or |card|): Value or reference to compare against

        Raises:
            Exception if the :param other: is invalid.

        Returns:
            bool: True if |self| is less than :param other:, False otherwise

        Compare the rank value of a :type str: or :type int: against
        |self|'s rank. If :param other: is a |card|, both suit and rank must be
        equal.
        """
        rank, other_rank = self._calculate_rank(other)

        if rank < other_rank:
            return True
        return False

    def __le__(self, other):
        """Determine if a card is less than or equal to a given value

        Args:
            other (int or str or |card|): Value or reference to compare against

        Raises:
            Exception if the :param other: is invalid.

        Returns:
            bool: True if |self| is less than or equal to :param other:, False
            otherwise
        """
        return (self < other) or (self == other)

    def __gt__(self, other):
        """Determine if a card is less than or equal to a given value

        Args:
            other (int or str or |card|): Value or reference to compare against

        Raises:
            Exception if the :param other: is invalid.

        Returns:
            bool: True if |self| is greater than :param other:, False otherwise
        """

        return (not self < other) and (not self == other)

    def __ge__(self, other):
        """Determine if a card is less than or equal to a given value

        Args:
            other (int or str or |card|): Value or reference to compare against

        Raises:
            Exception if the :param other: is invalid.

        Returns:
            bool: True if |self| is greater than or equal to :param other:,
            False otherwise
        """
        return (self > other) or (self == other)

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck(object):
    """Deck: A Deck of Playing Cards

    A container for |card| objects. If you need persistence, use the
    DeckModel.create_deck.
    """

    @staticmethod
    def get(id):
        """Retrieve a saved Deck

        Args:
            id (str): A UUID associated with a saved Deck

        Returns:
            Deck: a Deck with UUID id

        Raises:
            NoSuchDeckException if the Deck does not exist
        """
        try:
            deck_model = DeckModel.objects.get(pk=id)
        except Exception:
            raise NoSuchDeckException("No Such Deck Exists")

        decoded_deck = deck_model.decode()
        decoded_deck.deck_model = deck_model
        return decoded_deck

    def __init__(self, n = 1, cards = None, pile = None,
                 deck_model = None, shuffle = True):
        """Initialize a Deck: Deck(n, cards, pile, deck_model, shuffle)

        Attributes:
            pile (Pile): A container for discarded Cards

            deck_model (DeckModel): An object that manages the a Deck's
            persistence functions

            encoder (DeckEncoder): An object that knows how to encode a Deck

            cards (Card list): The Deck's cards

            count (int): The total number of cards in the Deck

        Keyword Args:
            n (int): Initialize the Deck with 52 * n cards. n must be greater
            than or equal to 1

            cards (Card list or None): Use a list of Card objects to populate
            the Deck.

            pile (Pile or None): Use a Pile for the Deck's pile
        """
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
        """
        Returns:
            str: A UUID in string format

        Raises:
            Exception if no ID is set.

        The UUID-formatted identifier for the Deck. Note that this is a
        property.
        """
        if self.deck_model:
            return str(self.deck_model.id)
        else:
            raise Exception("No ID set: Use DeckModel.create_deck() instead")

    def __iter__(self):
        return iter(self.cards)

    def shuffle(self):
        """Shuffle the cards of the deck

        Returns:
            None: This method mutates the ordering of the cards

        Randomize the ordering of the Deck's cards.
        """
        random.shuffle(self.cards)

    def _search(self, till):
        """Search for a card in the Deck

        Args:
            till (Card): A card to search the Deck for.

        Returns:
            int: The index of the card in the cards list, or -1 if the Deck
            contains to such card.

        This function helps implement some of the draw method's functionality.
        """
        for i, card in enumerate(self):
            if card == till:
                return i
        return -1

    def draw(self, n = 1, till = None, from_pile = None):
        if from_pile:
            return self.pile.draw(n=n, from_pile=from_pile)

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
        self.piles = piles or {self.DEFAULT_PILE: []}

    def count(self, pile = None):
        if not pile:
            pile = self.DEFAULT_PILE
        the_pile = self.piles[pile]
        return len(the_pile)

    def push(self, card, into = None):
        try:
            pile = self.piles[into]
        except KeyError:
            try:
                if not into:
                    pile = self.piles[self.DEFAULT_PILE]
                else:
                    self.piles[into] = pile = []
            except:
                raise Exception("Could not a create pile with that name.")

        try:
            if all([isinstance(c, Card) for c in card]):
                for c in card:
                    pile.append(c)
            else:
                raise Exception("There is a non-card in this pile")
        except TypeError:
            if isinstance(card, Card):
                pile.append(card)
            else:
                raise Exception("You may only discard a Card or a list of Cards")

    def draw(self, n = 1, from_pile = None):
        from_pile = from_pile or self.DEFAULT_PILE

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
        return self.piles.get(pile, self.piles[self.DEFAULT_PILE])

    def __repr__(self):
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
