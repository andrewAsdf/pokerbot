from copy import deepcopy
from mcts.mcts import MCTS
from mcts.graph import StateNode
from mcts.tree_policies import UCB1
from mcts.default_policies import random_terminal_roll_out
from mcts.backups import monte_carlo


class TreeNode:

    def __init__(self, game_state, our_seat):
        self.parent = None
        self.children = []
        self.visits = 1
        self.reward = 0

        self.state = deepcopy(game_state)
        self.our_seat = our_seat


    def perform(self, action_int):
        new_node = TreeNode(self.state, self.our_seat)

        if action_int == 1:
            new_node.state.bet()
        elif action_int == 0:
            new_node.state.call()
        elif action_int == -1:
            new_node.state.fold()
        else:
            raise RuntimeError('Invalid action to perform!')

        return new_node


    def reward(self, parent, action):
        if not self.state.is_over():
            raise RuntimeError('Cannot get reward for running game!')

        our_player = self.state.table[self.our_seat]

        winners = self.state.get_winners()

        if our_player in winners:
            return self.state.pot / len(winners)
        else:
            return (our_player.chips_bet + our_player._total_chips_bet) * -1


    @property
    def actions(self):
        if self.state.possible_to_raise():
            return [-1, 0, 1]
        else:
            return [-1, 0]


    def is_terminal(self):
        return self.state.is_over()



def _node_UCT(node):
    n = node.visits
    r = node.reward
    t = node.parent.visits
    return r / n + 1.41 * math.sqrt(math.log(t) / n)


class MCTSDecisionMaker:

    def __init__(self, opponent_modeller, db):
        self.opponent_modeller = opponent_modeller
        self.db = db


    def get_action(self, game_state, our_seat, max_iter=2000):
        root = TreeNode(game_state, our_seat)

        for _ in range(max_iter):
            selected_node = self._select(root)


    def __call__(self, game_state):
        root = TreeNode(game_state)
        pass


    def _select(self, node): #UCT algorithm
        selected_node = node
        while not selected_node.children == []
            selected_node = max(selected_node.children, key = _node_UCT)
        return selected_node


    def _expand(self, node):

        pass


    def _simulate(self, node):
        pass


    def _backpropagate(self, node):
        pass
