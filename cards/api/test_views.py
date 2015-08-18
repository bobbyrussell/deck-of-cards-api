import json

from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.test import TestCase, Client

from .views import DeckCreateAPIView

from deck.models import DeckModel, Deck, Card


class TestDeckCreateAPIView(TestCase):

    def test_post(self):
        client = Client()
        response = client.post(reverse('api:deck_create'))

        self.assertEqual(response.status_code, 201)

        deck = json.loads(response.content)

        self.assertTrue(isinstance(deck, dict))
        self.assertEqual(deck.get('count'), 52)

    def test_post_with_count(self):
        # use the count parameter to initialize a deck with 10 cards
        client = Client()
        url = reverse('api:deck_create') + '?count=10'
        response = client.post(url)

        self.assertEqual(response.status_code, 201)

        count = json.loads(response.content).get('count')

        self.assertEqual(count, 52 * 10)

        # use the count parameter to initialize a deck with 10 cards
        url = reverse('api:deck_create') + '?count=foobar'
        response = client.post(url)

        self.assertEqual(response.status_code, 409)


    def test_post_with_shuffle(self):
        client = Client()

        # if the deck is not shuffled, we should expect a Queen of Spades
        url = reverse('api:deck_create') + '?shuffle=False'
        response = client.post(url)

        self.assertEqual(response.status_code, 201)

        id = json.loads(response.content).get('id')
        deck = Deck.get(id)
        card = deck.draw()

        self.assertEqual(card, Card("Queen", "Spades"))

        # if the shuffle param is not "true" or "false", return an error
        url = reverse('api:deck_create') + '?shuffle=42'
        response = client.post(url)

        self.assertEqual(response.status_code, 409)

class TestDeckDetailAPIView(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_get(self):
        client = Client()
        response = client.get(reverse('api:deck_detail', args=(self.id,)))

        self.assertEqual(response.status_code, 200)

        deck = json.loads(response.content)
        self.assertTrue(isinstance(deck, dict))
        self.assertEqual(deck.get('count'), 52)


class TestDeckDraw(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_put(self):
        client = Client()

        url = reverse('api:deck_draw', args=(self.id,))
        response = client.put(url)
        self.assertEqual(response.status_code, 200)

        # draw 7 cards
        url = "{}{}".format(reverse('api:deck_draw', args=(self.id,)),
                            "?count=7")
        response = client.put(url)
        decoded_response = json.loads(response.content)

        for card in decoded_response.get('cards'):
            self.assertTrue(isinstance(card, dict))

        # attempt to draw more cards from the deck than there are in the deck
        url = "{}{}".format(reverse('api:deck_draw', args=(self.id,)),
                            "?count={}".format(self.deck.count + 1))
        response = client.put(url)

        self.assertEqual(response.status_code, 409)


class TestDeckShuffle(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_put(self):
        client = Client()
        url = reverse('api:deck_shuffle', args=(self.id,))
        response = client.put(url)

        self.assertEqual(response.status_code, 200)

class TestDeckDelete(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_put(self):
        client = Client()
        url = reverse('api:deck_delete', args=(self.id,))
        response = client.delete(url)

        self.assertEqual(response.status_code, 200)
        self.assertRaises(Exception, Deck.get, self.id)


class TestDiscardHand(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_put(self):
        # create some cards and discard them
        client = Client()
        cards = [{'rank': "Ace", 'suit': "Spades"},
                 {'rank': 2, 'suit': "Diamonds"}]
        url = reverse('api:deck_discard', args=(self.id,))
        response = client.put(url, data=json.dumps(cards),
                              content_type='application/json')

        self.assertEqual(response.status_code, 200)

        deck = Deck.get(self.id)
        decoded_cards = [Card("Ace", "Spades"), Card(2, "Diamonds")]

        for card in decoded_cards:
            self.assertIn(card, deck.pile.piles['discard'])

        # make sure data gets put into the endpoint
        url = reverse('api:deck_discard', args=(self.id,))
        response = client.put(url, content_type='application/json')

        self.assertEqual(response.status_code, 409)

        # make sure data that IS put it is valid
        url = reverse('api:deck_discard', args=(self.id,))
        data = [{'foo': 42, 'bar': 'baz'}]
        response = client.put(url, data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 409)
        deck = Deck.get(self.id)

    def test_put_with_named_pile(self):
        # create some cards and discard them
        client = Client()
        cards = [{'rank': "Ace", 'suit': "Spades"},
                 {'rank': 2, 'suit': "Diamonds"}]
        url = reverse('api:deck_discard', args=(self.id,)) + '?into=my+pile'
        response = client.put(url, data=json.dumps(cards),
                              content_type='application/json')

        self.assertEqual(response.status_code, 200)

        deck = Deck.get(self.id)
        decoded_cards = [Card("Ace", "Spades"), Card(2, "Diamonds")]

        for card in decoded_cards:
            self.assertIn(card, deck.pile.piles['my pile'])
