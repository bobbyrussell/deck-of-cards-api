from django.test import TestCase

from .models import Card, Deck, DeckModel
from .encoders import CardEncoder, DeckEncoder, CardDecoder, DeckDecoder

class TestCard(TestCase):

    def setUp(self):
        self.card = Card("Ace", "Spades")

    def test_card(self):
        # confirm that the card has a suit and a rank
        self.assertEquals(self.card.rank, "Ace")
        self.assertEquals(self.card.suit, "Spades")

    def test_encoding(self):
        # make sure that cards properly encode and decode
        encoded_card = CardEncoder().encode(self.card)
        decoded_card = CardDecoder().decode(encoded_card)
        self.assertEqual(self.card, decoded_card)
        self.assertEquals(decoded_card.rank, "Ace")
        self.assertEquals(decoded_card.suit, "Spades")

    def test_comparison(self):
        new_card = Card(5, "Clubs")
        self.assertTrue(new_card <= 5)
        self.assertTrue(new_card >= 5)
        self.assertTrue(new_card == 5)
        self.assertTrue(new_card > 4)
        self.assertTrue(new_card  < 6)
        self.assertTrue(self.card > new_card)


class TestDeck(TestCase):

    def setUp(self):
        self.deck = Deck()
        self.double_deck = Deck(2)

    def test_decoding(self):
        # confirm that decoding and encoding doesn't break anything
        encoded_deck = DeckEncoder().encode(self.deck)
        decoded_deck = DeckDecoder().decode(encoded_deck)
        self.assertEqual(decoded_deck.count, self.deck.count)

        cards = self.deck.draw(52)
        decoded_cards = decoded_deck.draw(52)
        self.assertEqual(len(cards), len(decoded_cards))

        for i in range(0, len(cards)):
            self.assertEqual(cards[i], decoded_cards[i])

    def test_deck(self):
        # draw a card
        card = self.deck.draw()

        # cofirm that the card is valid
        self.assertTrue(card.suit in ["Hearts", "Clubs", "Diamonds", "Spades"])
        self.assertTrue(1 <= card <= 13)

        # confirm that a deck has some cards in it
        self.assertTrue(self.deck.has_cards())
        self.assertEqual(self.deck.count, 51)

        # confirm that drawing decrements the card count
        self.deck.draw(self.deck.count)
        self.assertFalse(self.deck.has_cards())
        self.assertEqual(self.deck.count, 0)

        # confirm that overloading works
        self.assertEqual(self.double_deck.count, 52 * 2)
        cards = self.double_deck.draw(2)
        self.assertEqual(len(cards), 2)
        self.assertEqual(self.double_deck.count, (52 * 2) - 2)

        # confirm that discarding works
        card = cards.pop()
        self.deck.discard(card)
        self.assertEqual(self.deck.pile.draw(), card)

class TestDeckModel(TestCase):
    pass
