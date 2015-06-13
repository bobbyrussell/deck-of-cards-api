import json

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .views import DeckCreateAPIView

from deck.models import DeckModel


class TestDeckCreateAPIView(TestCase):

    def test_post(self):
        client = Client()
        response = client.post(reverse('deck_api_create'))
        self.assertEqual(response.status_code, 201)

class TestDeckDetailAPIView(TestCase):

    def setUp(self):
        self.deck = DeckModel.create_deck()
        self.id = self.deck.id

    def test_get(self):
        client = Client()
        response = client.get(reverse('deck_api_detail', args=(self.id,)))
        self.assertEqual(response.status_code, 200)
