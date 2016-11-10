pokerbot
========

Overview
--------

This is a project for my BSc. thesis. The goal of this project is to build a
computer poker agent which employs the MCTS algorithm for decision making, and
some machine-learning based opponent modelling.

The bot is written for PokerAcademy 2.5, but it uses
[meerkat-webclient](http://github.com/andrewAsdf/meerkat-webclient) to connect
to the game, so it's written in Python instead, and uses Flask.

Usage
-----

No automated install was created yet, so you have to install dependencies first:

```
sudo pip install -r ./requirements.txt
```

You need to have MongoDB installed, and running on your computer. You can start
the bot with the flask script:

```
export FLASK_APP = ./pokerbot/server.py
flask run
```

You can run the tests with `pytest`.
