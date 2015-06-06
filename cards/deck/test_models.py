from django.test import TestCase

from .models import Card, Deck

class TestCard(TestCase):

    def setUp(self):
        self.card = Card("Ace", "Spades")

    def test_card(self):
        self.assertEquals(self.card.rank, "Ace")
        self.assertEquals(self.card.suit, "Spades")

        other_card = Card("Ace", "Spades")
        self.assertEquals(self.card, other_card)

        self.assertTrue(self.card.is_black())
        self.assertFalse(self.card.is_red())

    def test_comparison(self):
        new_card = Card(5, "Clubs")
        self.assertTrue(new_card > 4)
        self.assertTrue(new_card <= 5)
        self.assertTrue(new_card >= 4)
        self.assertTrue(new_card == 4)
        self.assertTrue(new_card < 6)


class TestDeck(TestCase):

    def setUp(self):
        self.deck = Deck()
        self.double_deck = Deck(2)

    def test_deck(self):
        # draw a card
        card = self.deck.draw()

        # cofirm that the card is valid
        self.assertTrue(card.suit in ["Hearts", "Clubs", "Diamonds", "Spades"])
        self.assertTrue(1 <= card <= 13)

        self.assertTrue(self.deck.has_cards())
        self.assertEqual(self.deck.count, 51)

        self.deck.draw(self.deck.count)
        self.assertFalse(self.deck.has_cards())
        self.assertEqual(self.deck.count, 0)

        self.assertEqual(self.double_deck.count, 52 * 2)
        cards = self.double_deck.draw(2)
        self.assertEqual(len(cards), 2)
        self.assertEqual(self.double_deck.count, (52 * 2) - 2)

        card = cards.pop()
        self.deck.discard(card)
        self.assertEqual(self.deck.pile.draw(), card)
