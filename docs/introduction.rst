This is the documentation for the Deck of Cards API by Bobby Russell. 
Note that this is a small, simple, and currently incomplete implementation of a
Deck of Cards in the French Style.

What is the Deck of Cards API?
===============================

The Deck of Cards API is a pet project, inspired by the `Deck of Cards API`_ by
Chase Roberts.

There are two APIs to consider in this project: the REST API, and the Python
API. A a small subset of the Python API maps to the REST API.

============
The Deck API
============

The Deck API allows the user to interact with a subset of operations
available to a deck of cards. Players may create a deck of varying size (i.e.
with one or more full decks of cards,) draw from that deck, and discard into
piles associated with that deck.

============
The REST API
============

The REST API allows users to interact with the underlying Python API as a
service. Most of the Python API maps to a corresponding RESTful endpoint.

Why This Project?
=================

Modeling playing cards provided a fun and interesting exercise in API design.
The model of the 52 Card deck is widely known and simple to model, but at the
same time very rich. Using some light TDD allowed me to create an expressive
API that is fun to work with and easy to extend. Mapping the API to a
webservice seemed like a natural next step.

The Next Steps
==============

Aside from the previously mentioned features, I plan to add a simple game
client to demonstrate how one could use this API to create their own games!


.. _Deck of Cards API: https://github.com/crobertsbmw/deckofcards
.. _here: h
