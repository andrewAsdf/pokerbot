from pokerbot.decision_maker import MCTSDecisionMaker
from pokerbot.decision_maker import TreeNode
from pokerbot.decision_maker import CardNode
from pokerbot.decision_maker import BotNode
from pokerbot.decision_maker import OpponentNode
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
            return self.vpips[name]
        else:
            raise RuntimeError('Stat name should be "vpip"')


class MockCardProvider:

    def __init__(self, seed = 420, no_shuffle = False):
        self.random = Random(seed)
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
            self.random.shuffle(self.cards)


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

    def __init__(self):
        self.random = Random(420)

    def get_prediction(self, game_state):
        name = game_state.table.current_seat.name

        if name == 'Blaine':
            return self.random.choice([0, 1])
        elif name == 'Carly':
            return self.random.choice([-1, 0, 1])
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
                MockDB(), MockCardProvider(), pseudo_random = True)
        self.game = GameState()
        self.game.table[0] = Seat('Andy', 9999, ['As', 'Ad'])
        self.game.table[1] = Seat('Blaine', 9999)
        self.game.table[2] = Seat('Carly', 9999)
        self.game.new_game(0)


    def test_card_node(self):
        self.game.card_provider = MockCardProvider(no_shuffle = True)
        self.game.call()
        self.game.call()
        self.game.call()
        card_node = CardNode(self.game, 0)
        child_node, is_new  = card_node.get_child()

        assert is_new
        assert child_node.state.table.board == ['Ah', 'Kh', 'Qh']

        _, is_new  = card_node.get_child()
        assert child_node == card_node.get_child()[0]
        assert not is_new
        #it should return the same node


    def test_bot_node(self):
        self.game.card_provider = MockCardProvider(no_shuffle = True)
        bot_node = BotNode(self.game, 0)
        child_node, is_new  = bot_node.get_child()

        assert is_new
        bot_node.children.index(child_node)

        _, is_new  = bot_node.get_child()
        assert child_node == bot_node.get_child()[0]
        assert not is_new


    def test_opponent_node(self):
        self.game.card_provider = MockCardProvider(no_shuffle = True)
        player_node = OpponentNode(self.game, 0)
        child_node, is_new  = player_node.get_child([0.3,0.3,0.4])

        assert is_new
        player_node.children.index(child_node)

        _, is_new  = player_node.get_child([0.3,0.3,0.4])
        assert not is_new


    def test_get_action(self):
        self.decision_maker.get_action(self.game, max_iter = 200)



def make_node(node, graph, action):
    node_label = 'r: {}, v: {} p: {}, a: {}, s: {}'
    formatted_label = node_label.format(node.reward, node.visits,
            node.state.table.current_seat.name, action, node.state.stage)

    graph.node(str(hash(node)), formatted_label)


def get_graph(root, graph):
    nodes = deque()
    nodes.append(root)

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
    test = TestDecisionMaker()
    test.setup_method()
    test.test_get_action()

    graph = Digraph()
    graphviz_graph = get_graph(test.decision_maker.root, graph)
    graph.view()

