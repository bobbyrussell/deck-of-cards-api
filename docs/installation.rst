Installation
============

To run or fork or whatever a version of this code, we need only run a handful
of commands. Here's an install script that you can use:

.. code-block:: bash

    #!/bin/bash
    set -e

    # make a project directory and cd into it
    mkdir cards-api && cd cards-api

    # create a sandbox and activate it
    virtualenv env && . env/bin/activate

    # pull down the repo and cd into it
    git clone https://github.com/bobbyrussell/deck-of-cards-api
    cd deck-of-cards-api

    # install the project dependencies: pip for python, bower for front end
    pip install -r requirements/base.txt
    bower install

    # you will need to enter your user info with this invocation
    python cards/manage.py syncdb

    # finally, you're ready to go
    python cards/manage.py runserver

From here, you can point your browser to http://localhost:8000 and poke about.
