import re

from django.conf.urls import patterns, include, url

from .views import DeckCreateAPIView, DeckDetailAPIView, DeckDrawAPIView, \
                   DeckShuffleAPIView, DeckDeleteAPIView, DeckDiscardAPIView


urlpatterns = patterns('',
    url(r'^deck/new/?$', DeckCreateAPIView.as_view(), name='deck_create'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/?$',
          DeckDetailAPIView.as_view(), name='deck_detail'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/draw/?$',
          DeckDrawAPIView.as_view(), name='deck_draw'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/shuffle/?$',
          DeckShuffleAPIView.as_view(), name='deck_shuffle'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/delete/?$',
          DeckDeleteAPIView.as_view(), name='deck_delete'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/discard/?$',
          DeckDiscardAPIView.as_view(), name='deck_discard'),
)
