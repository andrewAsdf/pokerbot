from pokerbot.decision_maker import MCTSDecisionMaker
from pokerbot.decision_maker import TreeNode
from pokerbot.game_model import GameState
from pokerbot.game_model import Seat
from random import Random
from copy import copy
import logging
from graphviz import Digraph
from collections import deque

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
            return self.vpips['name']
        else:
            raise RuntimeError('Stat name should be "vpip"')


class MockCardProvider:

    def __init__(self, seed = 420):
        self.random = Random(seed)
        self.reset()


    def get_hand(self):
        return [self.cards.pop(), self.cards.pop()]


    def get_flop(self):
        return [self.cards.pop(), self.cards.pop(), self.cards.pop()]


    def get_turn(self):
        return self.cards.pop()


    def get_river(self):
        return self.cards.pop()


    def peek_cards(number):
        return self.cards[-number:]


    def shuffle(self):
        self.random.shuffle(self.cards)


    def reset(self):
        self.cards = [ '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td',
            'Jd', 'Qd', 'Kd', 'Ad', '2c', '3c', '4c', '5c', '6c', '7c', '8c',
            '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac', '2s', '3s', '4s', '5s', '6s',
            '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As', '2h', '3h', '4h',
            '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah' ]
        self.shuffle()


    def remove_cards(self, removed_cards):
        [self.cards.remove(c) for c in removed_cards]


    def copy(self):
        new_prov = copy(self)
        new_prov.cards = copy(self.cards)
        return new_prov


class MockOpponentModeller:

    def __init__(self):
        self.random = Random(420)

    def get_prediction(self, game_state):
        name = game_state.table.current_seat.name

        if name == 'Blaine':
            return self.random.choice([0, 1])
        elif name == 'Carly':
            return self.random.choice([-1, 0, 1])


class TestDecisionMaker:

    def setup_method(self):
        self.decision_maker = MCTSDecisionMaker(MockOpponentModeller(),
                MockDB(), MockCardProvider(), pseudo_random = True)
        self.game = GameState()
        self.game.table[0] = Seat('Andy', 9999, ['As', 'Ad'])
        self.game.table[1] = Seat('Blaine', 9999)
        self.game.table[2] = Seat('Carly', 9999)
        self.game.new_game(0)


    def test_get_best_action(self):
        self.root = TreeNode(self.game, 0)
        child1 = self.root.create_child(-1)
        child1.reward = 3
        child2 = self.root.create_child(0)
        child2.reward = 2
        child3 = self.root.create_child(1)
        child3.reward = 1

        assert self.root.get_best_action() == -1


    def test_get_action(self):
        self.decision_maker.get_action(self.game)



def get_graph(root, graph):
    nodes = deque()
    nodes.append(root)

    while nodes:
        node = nodes.popleft()

        action = 'x'

        if node.parent is not None:
            graph.edge(str(hash(node.parent)), str(hash(node)))
            action_index = node.parent.children.index(node)
            action = str(node.parent._children_actions[action_index])

        graph.node(str(hash(node)), 'r: {}, v: {} p: {}, a: {}, s: {}'.format(node.reward,
            node.visits, node.state.table.current_seat.name, action, node.state.stage))

        [nodes.append(c) for c in node.children]


if __name__ == '__main__':
    test = TestDecisionMaker()
    test.setup_method()
    test.test_get_action()

    graph = Digraph()
    graphviz_graph = get_graph(test.decision_maker.root, graph)
    graph.view()

