from flask import Flask
from flask import request
from flask import Response

import untangle
import json

import pokerbot.game_model
import pokerbot.database

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


db = pokerbot.database.Database()

game = pokerbot.game_model.GameState()

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

    our_seat = int(xml.holecards.seat.cdata)
    game.our_seat = our_seat

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
    game.table.clear()
    actions.clear()

    xml = getObjectFromXmlData(request.data)

    for p in xml.newgame.players.player:
        seat = int(p.seat.cdata)
        game.table[seat].name = p.name.cdata
        game.table[seat].stack = float(p.stack.cdata)

    game.table.button_seat = int(xml.newgame.buttonseat.cdata)

    return Response()


@app.route('/showdown', methods=['POST'])
def showdown_event():
    xml = getObjectFromXmlData(request.data)

    for hand in xml.showdown.cards:
        cards = [x.cdata for x in hand.card]

        seatnumber = int(hand.seat.cdata)
        game.table.seats[seatnumber].hand = cards

    return Response()


@app.route('/board', methods=['POST'])
def board():
    xml = getObjectFromXmlData(request.data)

    game.stage = xml.board.stage.cdata

    game.table.board = [x.cdata for x in xml.board.cards.card]

    return Response()


@app.route('/gameover', methods=['POST'])
def gameover():

    seats = [{'name': seat.name, 'seat_number': i, 'hand': seat.hand} for i, seat\
            in enumerate(game.table.seats) if not seat.empty()]

    db.add_game(seats, actions, game.table.button_seat)
    return Response()


if __name__ == '__main__':
    app.run()
