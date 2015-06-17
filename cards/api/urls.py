import re

from django.conf.urls import patterns, include, url

from .views import DeckCreateAPIView, DeckDetailAPIView, DeckDrawAPIView, \
                   DeckShuffleAPIView, DeckDeleteAPIView


urlpatterns = patterns('',
    url(r'^deck/new/?$', DeckCreateAPIView.as_view(), name='deck_api_create'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/?$',
          DeckDetailAPIView.as_view(), name='deck_api_detail'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/draw/?$',
          DeckDrawAPIView.as_view(), name='deck_api_draw'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/shuffle/?$',
          DeckShuffleAPIView.as_view(), name='deck_api_shuffle'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/delete/?$',
          DeckDeleteAPIView.as_view(), name='deck_api_delete'),
)
