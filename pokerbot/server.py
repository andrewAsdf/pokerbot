from flask import Flask
from flask import request
from flask import Response

from pokerbot.controller import Controller
from pokerbot.database import Database
from pokerbot.game_model import GameState
from pokerbot.game_model import Seat

import untangle
import json

app = Flask(__name__)

action_string = '<?xml version="1.0" encoding="UTF-8"?>\
                <action>\
                    <type>{}</type>\
                    <amount>{}</amount>\
                </action>'

def getActionXml(action_type, amount=0):
    return action_string.format(action_type, amount)


def getObjectFromXmlData(data):
    data_str = data.decode()
    return untangle.parse(data_str)


controller = Controller(GameState(), Database())


@app.route('/', methods=['GET'])

def index():
    game = controller.game

    player_seats = [s for s in game.table.seats if not s.empty]
    items = [player_seats, controller.events, {'pot': game.pot, 'to_call':game.to_call}]

    gameText = json.dumps(items, default=vars, indent=2)

    return Response(gameText, mimetype='text/plain')


@app.route('/holecards', methods=['POST'])
def hole_cards():

    xml = getObjectFromXmlData(request.data)
    cards = xml.holecards.cards.card #an array of 2 cards

    controller.bot_seat(int(xml.holecards.seat.cdata))
    controller.bot_cards((cards[0].cdata, cards[1].cdata))

    return Response()


@app.route('/action', methods=['GET', 'POST'])
def action():

    if request.method == 'GET':
        xml = getActionXml ('raise', 10)
        return Response(xml, mimetype='text/xml');
    else:
        xml = getObjectFromXmlData(request.data)
        action = {}
        action['seat'] = xml.action.seat.cdata
        action['type'] = xml.action.type.cdata
        try:
            action['amount'] = xml.action.amount.cdata
        except IndexError:
            pass

        controller.receive_event(action)
        return Response()


@app.route('/newgame', methods=['POST'])
def newgame():

    xml = getObjectFromXmlData(request.data)

    players = [Seat()] * 10

    for p in xml.newgame.players.player:
        seat = int(p.seat.cdata)
        players[seat] = Seat(p.name.cdata, float(p.stack.cdata))

    button_seat = int(xml.newgame.buttonseat.cdata)
    controller.new_game(players, button_seat)
    return Response()


@app.route('/showdown', methods=['POST'])
def showdown_event():
    xml = getObjectFromXmlData(request.data)

    for hand in xml.showdown.cards:
        cards = [x.cdata for x in hand.card]
        seat = int(hand.seat.cdata)
        controller.show_cards(seat, cards)

    return Response()


@app.route('/board', methods=['POST'])
def board():
    xml = getObjectFromXmlData(request.data)

    stage = xml.board.stage.cdata
    cards = [x.cdata for x in xml.board.cards.card]

    controller.receive_event({'type': 'board', 'stage': stage, 'cards': cards})

    return Response()


@app.route('/gameover', methods=['POST'])
def gameover():
    controller.game_over()
    return Response()


if __name__ == '__main__':
    app.run()
