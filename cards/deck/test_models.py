from django.test import TestCase

from .models import Card, Deck, DeckModel
from .encoders import DeckEncoder, CardDecoder, DeckDecoder, CardEncoder

class TestCard(TestCase):

    def setUp(self):
        self.ace_of_spades = Card("Ace", "Spades")
        self.five_of_clubs = Card(5, "Clubs")
        self.two_of_hearts = Card(2, "Hearts")

    def test_card(self):
        # confirm that the card has a suit and a rank
        self.assertEqual(self.ace_of_spades.rank, "Ace")
        self.assertEqual(self.ace_of_spades.suit, "Spades")

    def test_encoding(self):
        # make sure that cards properly encode and decode
        encoded_card = CardEncoder().encode(self.ace_of_spades)
        decoded_card = CardDecoder().decode(encoded_card)
        self.assertEqual(self.ace_of_spades, decoded_card)
        self.assertEqual(decoded_card.rank, "Ace")
        self.assertEqual(decoded_card.suit, "Spades")

    def test_lt_comparisons(self):
        self.assertTrue(self.five_of_clubs <= 5)
        self.assertFalse(self.five_of_clubs < 5)
        self.assertTrue(self.five_of_clubs < 6)

        self.assertTrue(self.five_of_clubs <= "Ace")
        self.assertTrue(self.five_of_clubs < "Ace")

        self.assertTrue(self.five_of_clubs <= self.ace_of_spades)
        self.assertTrue(self.five_of_clubs < self.ace_of_spades)
        self.assertFalse(self.five_of_clubs <= self.two_of_hearts)
        self.assertFalse(self.five_of_clubs < self.two_of_hearts)

    def test_gt_comparisons(self):
        self.assertFalse(self.five_of_clubs > 5)
        self.assertTrue(self.five_of_clubs >= 5)
        self.assertTrue(self.five_of_clubs >= 4)

        self.assertTrue(self.ace_of_spades >= "King")

        self.assertTrue(self.five_of_clubs > self.two_of_hearts)
        self.assertTrue(self.five_of_clubs >= self.two_of_hearts)

        self.assertFalse(self.five_of_clubs > self.ace_of_spades)
        self.assertFalse(self.five_of_clubs > self.ace_of_spades)

    def test_eq_comparisons(self):
        self.assertFalse(self.five_of_clubs == 4)
        self.assertFalse(self.five_of_clubs == 6)
        self.assertTrue(self.five_of_clubs == 5)

        self.assertTrue(self.ace_of_spades == "Ace")

        ace_of_spades = Card("Ace", "Spades")
        self.assertTrue(self.ace_of_spades == ace_of_spades)


class TestDeck(TestCase):

    def setUp(self):
        self.deck = Deck()
        self.unshuffled_deck = Deck(shuffle=False)
        self.double_deck = Deck(2)
        self.ace_of_spades = Card("Ace", "Spades")

    def test_encoding(self):
        # confirm that decoding and encoding doesn't break anything
        encoded_deck = DeckEncoder().encode(self.deck)
        decoded_deck = DeckDecoder().decode(encoded_deck)
        self.assertEqual(decoded_deck.count, self.deck.count)

        # draw out both decks
        cards = self.deck.draw(52)
        decoded_cards = decoded_deck.draw(52)
        self.assertEqual(len(cards), len(decoded_cards))

        # run some more tests
        for i in range(0, len(cards)):
            self.assertTrue(isinstance(decoded_cards[i], Card))
            self.assertEqual(cards[i], decoded_cards[i])

    def test_deck(self):
        # draw a card
        card = self.deck.draw()

        # cofirm that the card is valid
        self.assertTrue(card.suit in ["Hearts", "Clubs", "Diamonds", "Spades"])
        self.assertTrue(2 <= card <= "Ace")

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

    def test_draw(self):
        queen = self.unshuffled_deck.draw()
        self.assertEqual(queen, Card("Queen", "Spades"))

        cards_until_ace = self.unshuffled_deck.draw(till=self.ace_of_spades)
        last_card = cards_until_ace[-1]
        self.assertEqual(last_card, self.ace_of_spades)
        self.assertEqual(self.unshuffled_deck.count + len(cards_until_ace) + 1, 
                         52)

        card = self.unshuffled_deck.draw()
        drawn_out_deck = self.unshuffled_deck.draw(till=card)
        self.assertFalse(self.unshuffled_deck.has_cards())
        self.assertRaises(Exception, self.unshuffled_deck.draw)

class TestDeckModel(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()

    def test_deck(self):
        self.assertEqual(self.deck.count, 52)
        hand = self.deck.draw(7)
        deck_id = self.deck.id
        self.deck.save()
        self.deck = None

        deck = Deck.get(deck_id)
        self.assertTrue(deck.count, 52 - 7)

        for card in deck:
            self.assertNotIn(card, hand)

        hand = deck.draw(7)
        self.assertTrue(deck.count, (52 - 7) -  7)
        self.assertEqual(deck.pile.count, 0)
        deck.discard(hand)
        self.assertEqual(deck.pile.count, 7)
        deck.save()
        deck = None

        deck = Deck.get(deck_id)
        self.assertTrue(deck.count, (52 - 7) -  7)
        self.assertEqual(deck.pile.count, 7)

        for card in deck:
            self.assertNotIn(card, hand)

        for card in hand:
            self.assertIn(card, deck.pile)
