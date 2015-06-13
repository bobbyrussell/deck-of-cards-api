import re

from django.conf.urls import patterns, include, url

from .views import DeckCreateAPIView, DeckDetailAPIView


urlpatterns = patterns('',
    url(r'^deck/new/?$', DeckCreateAPIView.as_view(), name='deck_api_create'),
    url(r'^deck/(?P<uuid>[0-9a-f\-]{36})/?$',
          DeckDetailAPIView.as_view(), name='deck_api_detail'),
)
