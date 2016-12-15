from pokerbot.decision_maker import MCTSDecisionMaker
from pokerbot.decision_maker import TreeNode
from pokerbot.decision_maker import CardNode
from pokerbot.decision_maker import BotNode
from pokerbot.decision_maker import OpponentNode
from pokerbot.game_model import GameState
from pokerbot.game_model import Seat
import random
from copy import copy
import logging
from graphviz import Digraph
from collections import deque
import time

def get_logger():
    logger = logging.getLogger('pokerbot')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(fmt)

    logger.addHandler(ch)
    return logger

logger = get_logger()

class MockDB:

    def __init__(self):
        self.vpips = {
            'Andy' :   0.8,
            'Blaine' : 0.4,
            'Carly' :  0.2
        }

    def get_player_stat(self, name, stat):
        if stat == 'vpip':
            return self.vpips[name]
        else:
            raise RuntimeError('Stat name should be "vpip"')


class MockCardProvider:

    def __init__(self, no_shuffle = False):
        self.no_shuffle = no_shuffle
        self.reset()


    def get_hand(self, vpip = 1):
        return [self.cards.pop(), self.cards.pop()]


    def get_flop(self):
        return [self.cards.pop(), self.cards.pop(), self.cards.pop()]


    def get_turn(self):
        return self.cards.pop()


    def get_river(self):
        return self.cards.pop()


    def peek_cards(self, number):
        return self.cards[-number:]


    def shuffle(self):
        if not self.no_shuffle:
            random.shuffle(self.cards)


    def reset(self):
        self.cards = [ '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td',
            'Jd', 'Qd', 'Kd', 'Ad', '2c', '3c', '4c', '5c', '6c', '7c', '8c',
            '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac', '2s', '3s', '4s', '5s', '6s',
            '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As', '2h', '3h', '4h',
            '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah' ]


    def remove_cards(self, removed_cards):
        [self.cards.remove(c) for c in removed_cards]


    def copy(self):
        new_prov = copy(self)
        new_prov.cards = copy(self.cards)
        return new_prov


class MockOpponentModeller:

    def get_prediction(self, game_state):
        name = game_state.table.current_seat.name

        if name == 'Blaine':
            return random.choice([0, 1])
        elif name == 'Carly':
            return random.choice([-1, 0, 1])
        else:
            raise RuntimeError()

    def get_probabilities(self, game_state):
        name = game_state.table.current_seat.name

        if name == 'Blaine':
            return [0, 0.5, 0.5]
        elif name == 'Carly':
            return [0.1, 0.7, 0.2]
        else:
            return None #it is called for every player, but discarded for our own player


class TestDecisionMaker:

    def setup_method(self):
        self.decision_maker = MCTSDecisionMaker(MockOpponentModeller(),
                MockDB(), MockCardProvider())
        self.game = GameState(auto_stage = True)
        self.game.table[0] = Seat('Andy', 9999, ['Qc', 'Js'])
        self.game.table[1] = Seat('Blaine', 9999)
        self.game.table[2] = Seat('Carly', 9999)
        self.game.new_game(0)
        random.seed(420)


    def test_get_action_preflop(self):
        assert self.game.table.current_seat.name == 'Andy'
        self.decision_maker.get_action(self.game, max_iter = 200)


    def test_get_action_flop(self):
        self.game.call()
        self.game.call()
        self.game.call()

        self.game.table.board = ['4s', 'Tc', '9c']

        self.game.call()
        self.game.call()
        assert self.game.table.current_seat.name == 'Andy'
        self.decision_maker.get_action(self.game, max_iter = 200)


    def test_get_action_turn(self):
        self.game.call()
        self.game.call()
        self.game.call()

        self.game.call()
        self.game.call()
        self.game.call()

        self.game.table.board = ['4s', 'Tc', '9c', 'Qs']

        self.game.call()
        self.game.call()
        assert self.game.table.current_seat.name == 'Andy'
        self.decision_maker.get_action(self.game, max_iter = 200)


    def test_get_action_river(self):
        self.game.call()
        self.game.call()
        self.game.call()

        self.game.call()
        self.game.call()
        self.game.call()

        self.game.call()
        self.game.call()
        self.game.call()

        self.game.table.board = ['4s', 'Tc', '9c', 'Qs', '5s']

        self.game.call()
        self.game.call()
        assert self.game.table.current_seat.name == 'Andy'
        self.decision_maker.get_action(self.game, max_iter = 200)



def make_node(node, graph, action):
    node_label = 'r: {}, v: {} p: {}, a: {}, s: {}'
    formatted_label = node_label.format(node.reward, node.visits,
            node.state.table.current_seat.name, action, node.state.stage)

    graph.node(str(hash(node)), formatted_label)


def get_graph(root, graph):
    nodes = deque()
    nodes.append(root)

    make_node(root, graph, 'x')

    while nodes:
        node = nodes.popleft()

        if type(node.children) is list:
            for i, child_node in enumerate(node.children):
                if child_node is not None:
                    nodes.append(child_node)
                    make_node(child_node, graph, i - 1)
                    graph.edge(str(hash(node)), str(hash(child_node)))

        elif type(node.children) is dict:
            for i, child_node in node.children.items():
                nodes.append(child_node)
                make_node(child_node, graph, i)
                graph.edge(str(hash(node)), str(hash(child_node)))


if __name__ == '__main__':

    decision_maker = MCTSDecisionMaker(MockOpponentModeller(),
            MockDB(), MockCardProvider())

    game = GameState(auto_stage = True)
    game.table[0] = Seat('Andy', 9999, ['Qc', 'Js'])
    game.table[1] = Seat('Blaine', 9999)
    game.table[2] = Seat('Carly', 9999)
    game.new_game(0)
    random.seed(420)

    assert game.table.current_seat.name == 'Andy'
    start_time = time.time()
    decision_maker.get_action(game, max_iter = 2000)
    print('MCTS running time: {} sec'.format(time.time() - start_time))

    #graph = Digraph()
    #graphviz_graph = get_graph(decision_maker.root, graph)
