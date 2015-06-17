import json

from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.test import TestCase, Client

from .views import DeckCreateAPIView

from deck.models import DeckModel, Deck


class TestDeckCreateAPIView(TestCase):

    def test_post(self):
        client = Client()
        response = client.post(reverse('deck_api_create'))
        self.assertEqual(response.status_code, 201)
        deck = json.loads(response.content)
        self.assertTrue(isinstance(deck, dict))
        self.assertEqual(deck.get('count'), 52)

    def test_post_with_count(self):
        client = Client()

        # use the count parameter to initialize a deck with 10 cards
        url = reverse('deck_api_create') + '?count=10'
        response = client.post(url)
        self.assertEqual(response.status_code, 201)
        count = json.loads(response.content).get('count')
        self.assertEqual(count, 52 * 10)


class TestDeckDetailAPIView(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_get(self):
        client = Client()
        response = client.get(reverse('deck_api_detail', args=(self.id,)))
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

        url = reverse('deck_api_draw', args=(self.id,))
        response = client.put(url)
        self.assertEqual(response.status_code, 200)

        # draw 7 cards
        url = "{}{}".format(reverse('deck_api_draw', args=(self.id,)),
                            "?count=7")
        response = client.put(url)
        decoded_response = json.loads(response.content)

        for card in decoded_response.get('cards'):
            self.assertTrue(isinstance(card, dict))

        # attempt to draw more cards from the deck than there are in the deck
        url = "{}{}".format(reverse('deck_api_draw', args=(self.id,)),
                            "?count={}".format(self.deck.count + 1))
        response = client.put(url)
        self.assertEqual(response.status_code, 409)


class TestDeckShuffle(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_put(self):
        client = Client()
        url = reverse('deck_api_shuffle', args=(self.id,))
        response = client.put(url)
        self.assertEqual(response.status_code, 200)

class TestDeckDelete(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_put(self):
        client = Client()
        url = reverse('deck_api_delete', args=(self.id,))
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(Exception, Deck.get, self.id)
