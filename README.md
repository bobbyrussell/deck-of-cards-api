# Deck of Cards API

This is the documentation for the Deck of Cards API by Bobby Russell. 
Note that this is a small, simple, and currently incomplete implementation of a
Deck of Cards in the French Style.

## What is the Deck of Cards API?

The Deck of Cards API is a pet project, inspired by Chase Roberts'
[Deck of Cards API](http://deckofcardsapi.com/). You can check out Chase's
implementation [here](https://github.com/crobertsbmw/deckofcards).

There are two APIs to consider in this project: the REST API, and the Python
API. A small subset of the Python API maps to the REST API.

## The Deck API

The Deck API allows the user to interact with a subset of operations
available to a deck of cards. Players may create a deck of varying size (i.e.
with one or more full decks of cards,) draw from that deck, and discard into
piles associated with that deck.

## The REST API

The REST API allows users to interact with the underlying Python API as a
service. Most of the Python API maps to a corresponding RESTful endpoint.

## Installation
You can build this project from source with the following commands:

    mkdir cards-api && cd cards-api
    virtualenv env && . env/bin/activate
    git clone https://github.com/bobbyrussell/deck-of-cards-api
    cd deck-of-cards-api
    pip install -r requirements/base.txt
    bower install
    python cards/manage.py syncdb
    python cards/manage.py runserver


## License
This code is licensed under the MIT License.
