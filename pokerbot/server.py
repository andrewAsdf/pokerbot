from pokerbot.controller import Controller
from pokerbot.database import Database
from pokerbot.game_model import GameState
from pokerbot.game_model import Seat
from pokerbot.opponent_modeller import OpponentModeller
from pokerbot.decision_maker import MCTSDecisionMaker
from pokerbot.card_provider import CardProvider
import pokerbot.stats
import pokerbot.features
import pokerbot.learning as learning

import logging
import untangle
import json
from flask import Flask
from flask import request
from flask import Response



def get_logger():
    logger = logging.getLogger('pokerbot')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('pokerbot.log')
    fh.setLevel(logging.DEBUG)

    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)

    logger.addHandler(fh)
    return logger

logger = get_logger()

app = Flask(__name__)

db = Database()

features = pokerbot.features.functions

opponent_modeller = OpponentModeller(features, db, 100, learning, pokerbot.stats)
decision_maker = MCTSDecisionMaker(opponent_modeller, db, CardProvider())

controller = Controller(GameState(), db, opponent_modeller, decision_maker)


action_string_template = '''<?xml version="1.0" encoding="UTF-8"?>
                                <action>
                                    <type>{}</type>
                                <amount>{}</amount>
                            </action>'''



def get_action_xml(action_type, amount=1):
    return action_string_template.format(action_type, amount)


def get_object_from_xml(data):
    data_str = data.decode()
    return untangle.parse(data_str)


@app.route('/', methods=['GET'])

def index():
    game = controller.game

    player_seats = [s for s in game.table.seats if not s.empty]

    if (controller.playing):
        features = pokerbot.features.get_features(game)
    else:
        features = None

    items = [
            player_seats,
            controller.events,
            {'pot': game.pot, 'to_call':game.to_call},
            features
    ]

    gameText = json.dumps(items, default=vars, indent=2)

    return Response(gameText, mimetype='text/plain')


@app.route('/holecards', methods=['POST'])
def hole_cards():

    xml = get_object_from_xml(request.data)
    cards = xml.holecards.cards.card #an array of 2 cards

    controller.bot_seat(int(xml.holecards.seat.cdata))
    controller.bot_cards([cards[0].cdata, cards[1].cdata])

    return Response()


def action_to_string(action_int):
    if action_int == -1:
        return 'fold'
    elif action_int == 0:
        return 'call'
    elif action_int == 1:
        return 'raise'
    else:
        raise RuntimeError('Invalid action integer!')


@app.route('/action', methods=['GET', 'POST'])
def action():

    if request.method == 'GET':
        action_int = controller.get_action()
        action = action_to_string(action_int)

        logger.info("Bot action is: {}".format(action))

        xml = get_action_xml (action, 10)
        return Response(xml, mimetype='text/xml');
    else:
        xml = get_object_from_xml(request.data)
        action = {}
        action['seat'] = int(xml.action.seat.cdata)
        action['type'] = xml.action.type.cdata
        try:
            action['amount'] = float(xml.action.amount.cdata)
        except IndexError:
            pass

        controller.receive_event(action)
        return Response()


@app.route('/newgame', methods=['POST'])
def newgame():

    xml = get_object_from_xml(request.data)

    players = [Seat() for _ in range(10)]

    for p in xml.newgame.players.player:
        seat = int(p.seat.cdata)
        players[seat] = Seat(p.name.cdata, float(p.stack.cdata))

    button_seat = int(xml.newgame.buttonseat.cdata)
    controller.new_game(players, button_seat)
    return Response()


@app.route('/showdown', methods=['POST'])
def showdown_event():
    xml = get_object_from_xml(request.data)

    for hand in xml.showdown.cards:
        cards = [x.cdata for x in hand.card]
        seat = int(hand.seat.cdata)
        controller.show_cards(seat, cards)

    return Response()


@app.route('/board', methods=['POST'])
def board():
    xml = get_object_from_xml(request.data)

    stage = xml.board.stage.cdata
    cards = [x.cdata for x in xml.board.cards.card]

    controller.receive_event({'type': 'board', 'stage': stage, 'cards': cards})

    return Response()


@app.route('/gameover', methods=['POST'])
def gameover():
    xml = get_object_from_xml(request.data)

    winning = xml.gameover.winning

    gameover_event = {}
    gameover_event['type'] = 'gameover'
    gameover_event['wins'] = {w.seat.cdata : float(w.amount.cdata) for w in winning}

    controller.receive_event(gameover_event)
    return Response()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
