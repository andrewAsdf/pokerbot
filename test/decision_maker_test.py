from pokerbot.decision_maker import MCTSDecisionMaker
from pokerbot.decision_maker import TreeNode
from pokerbot.game_model import GameState
from pokerbot.game_model import Seat
from random import Random
import logging

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

    def __init__(self):
        self.random = Random(420)
        self.shuffle()


    def get_hand(self):
        return [self.cards.pop(), self.cards.pop()]


    def get_flop(self):
        return [self.cards.pop(), self.cards.pop(), self.cards.pop()]


    def get_turn(self):
        return self.cards.pop()


    def get_river(self):
        return self.cards.pop()


    def shuffle(self):
        self.cards = [ '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td',
            'Jd', 'Qd', 'Kd', 'Ad', '2c', '3c', '4c', '5c', '6c', '7c', '8c',
            '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac', '2s', '3s', '4s', '5s', '6s',
            '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As', '2h', '3h', '4h',
            '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah' ]
        self.random.shuffle(self.cards)



class MockOpponentModeller:

    def __init__(self):
        self.random = Random(420)

    def get_prediction(self, game_state):
        name = game_state.table.current_seat.name
        can_raise = game_state.possible_to_raise

        if name == 'Blaine':
            return self.random.choice([0, 1])
        elif name == 'Carly':
            return self.random.choice([-1, 0, 1])



class TestTreeNode:

    def setup_method(self):
        self.root = TreeNode(None, 0)
        child1 = self.root.create_child(-1)
        child1.reward = 3
        child2 = self.root.create_child(0)
        child2.reward = 2
        child3 = self.root.create_child(1)
        child3.reward = 1


    def test_get_best_action(self):
        assert self.root.get_best_action() == -1




class TestDecisionMaker:

    def setup_method(self):
        self.decision_maker = MCTSDecisionMaker(MockOpponentModeller(),
                MockDB(), pseudo_random = True)
        self.game = GameState(card_provider = MockCardProvider())
        self.game.table[0] = Seat('Andy', 9999)
        self.game.table[1] = Seat('Blaine', 9999)
        self.game.table[2] = Seat('Carly', 9999)
        self.game.new_game()


    def test_get_action(self):
        self.decision_maker.get_action(self.game, 0)


if __name__ == '__main__':
    test = TestDecisionMaker()
    test.setup_method()
    test.test_get_action()
