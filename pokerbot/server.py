from flask import Flask
from flask import request
from flask import Response

import untangle
import json

import pokerbot.game_model

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


game = pokerbot.game_model.GameState()

table = game.table

our_seat = []

actions = []


@app.route('/', methods=['GET'])

def index():
    gameText = json.dumps(game, default=vars, indent=2)
    actionsText = json.dumps(actions, default=vars, indent=2)

    return Response(gameText + actionsText, mimetype='text/plain')


@app.route('/holecards', methods=['POST'])
def hole_cards():

    xml = getObjectFromXmlData(request.data)
    cards = xml.holecards.cards.card #an array of 2 cards
    global current_cards
    current_cards = (cards[0].cdata, cards[1].cdata)
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

        actions.append(action)
        return Response()


@app.route('/newgame', methods=['POST'])
def newgame():
    xml = getObjectFromXmlData(request.data)
    seat_number = int(xml.newgame.buttonseat.cdata)

    table.clear()
    actions.clear()

    for p in xml.newgame.players.player:
        seat = int(p.seat.cdata)
        table[seat].name = p.name.cdata
        table[seat].stack = float(p.stack.cdata)
        table[seat].empty = False

    global our_seat
    our_seat = table[seat_number]
    return Response()


@app.route('/showdown', methods=['POST'])
def showdown_event():
    xml = getObjectFromXmlData(request.data)

    for hand in xml.showdown.cards:
        cards = [x.cdata for x in hand.card]

        seatnumber = int(hand.seat.cdata)
        table.seats[seatnumber].cards = cards

    return Response()


@app.route('/board', methods=['POST'])
def stage_event():
    xml = getObjectFromXmlData(request.data)

    game.stage = xml.board.stage.cdata

    game.table.board = [x.cdata for x in xml.board.cards.card]

    return Response()


@app.route('/gameover', methods=['POST'])
def win_event():
    return 'GameOver'


if __name__ == '__main__':
    app.run()
