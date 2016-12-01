from numpy import random as np_rand
from deuces import Card
import math
import logging

logger = logging.getLogger('pokerbot.decision_maker')


class MCTSDecisionMaker:

    def __init__(self, opponent_modeller, db, card_provider, pseudo_random = False):
        self.opponent_modeller = opponent_modeller
        self.db = db
        self.card_provider = card_provider
        if pseudo_random:
            np_rand.seed(420)


    def get_action(self, game_state, max_iter=2000):
        logger.info('MCTS iteration count: {}'.format(max_iter))
        logger.info('Getting decision for player {}'
                .format(game_state.table.current_seat.name))

        our_seat = game_state.table.current_index
        self.root = BotNode(game_state, our_seat)

        assert self.root.state.auto_stage == False
        self._assign_card_provider(self.root)

        for i in range(max_iter):
            if not (i + 1) % 500:
                logger.info('MCTS iteration: {}'.format(i + 1))

            self._do_iteration(self.root)

        action = self.root.get_best_action()
        logger.info('Chosen action: {}'.format(action))
        return action


    def _do_iteration(self, root):
        new_node = self._get_new_node(root)
        reward = self._simulate(new_node)
        self._backpropagate(new_node, reward)


    def _get_new_node(self, root):
        node, is_new = root.get_child()

        while not (is_new or node.is_terminal):
            node, is_new = node.get_child(self.opponent_modeller.get_probabilities())

        return node


    def _simulate(self, node):
        simulation_node = node.copy()
        simulation_node.state.auto_stage = True
        simulation_node.state.card_provider.shuffle()

        while not simulation_node.is_terminal():
            if simulation_node.our_turn():
                choice = np_rand.choice(simulation_node.actions) #TODO: apply an OM instead
                simulation_node.perform(choice)
            else:
                prediction = self._get_prediction(simulation_node)
                simulation_node.perform(prediction)

        return simulation_node.get_reward()


    def _backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent


    def _get_prediction(self, node):
        prediction = self.opponent_modeller.get_prediction(node.state)
        if prediction in node.actions:
            return prediction
        else: #this occurs when predictor tells to raise but it is not a valid move
            return 0


    def _get_probabilities(self, node):
        probabilities = self.opponent_modeller.get_probabilities(node.state)
        if len(node.actions) == 2: #when raise is not available
            probabilities[2] = 0
        return probabilities


    def _assign_card_provider(self, node):
        self.card_provider.reset()
        our_cards = node.state.table[node.our_seat].hand
        board_cards = node.state.table.board
        self.card_provider.remove_cards(our_cards + board_cards)
        node.state.card_provider = self.card_provider


class TreeNode:

    def __init__(self, game_state, our_seat):
        self.parent = None
        self.visits = 1
        self.reward = 0

        self.state = game_state.copy()
        self.our_seat = our_seat


    def perform(self, action_int):
        if action_int == 1:
            self.state.bet()
        elif action_int == 0:
            self.state.call()
        elif action_int == -1:
            self.state.fold()
        else:
            raise RuntimeError('Invalid action to perform!')


    def copy(self):
        return TreeNode(self.state, self.our_seat)


    def get_reward(self):
        if not self.state.is_over():
            raise RuntimeError('Cannot get reward for running game!')
        return get_reward(self.state, self.our_seat)


    def _node_UCT(self, node):
        if node is None:
            return 1.41 * math.sqrt(math.log(self.visits))
        else:
            n = node.visits
            r = node.reward
            return r / n + 1.41 * math.sqrt(math.log(self.visits) / n)


    def our_turn(self):
        return self.state.table.current_index == self.our_seat


    def is_terminal(self):
        return self.state.is_over()


    def stage_over(self):
        return self.state.stage_over()


def _create_new_node(node):
    '''Create a new node using the state found in node.'''

    if node.stage_over():
        return CardNode(node.state, node.our_seat)
    elif not node.our_turn():
        return OpponentNode(node.state, node.our_seat)
    else:
        return PlayerNode(node.state, node.our_seat)


class PlayerNode(TreeNode):

    _player_actions = [-1, 0, 1]
    _player_actions_noraise = [-1, 0]


    def __init__(self, game_state, our_seat):
        self.children = [None, None, None]
        super.__init__(game_state, our_seat) 


    def _create_child(self, index):
        new_node = _create_new_node(self)
        new_node.parent = self
        self.children[index] = new_node
        new_node.perform(self._index_to_action(index))
        return new_node


    @property
    def actions(self):
        if self.state.possible_to_raise():
            return self._player_actions
        else:
            return self._player_actions_noraise


    def get_best_action(self, key = PlayerNode._child_value):
        best_child = max(self.children, key=key)
        index = self.children.index(best_child)
        return self._index_to_action(index)


    @staticmethod
    def _child_value(node):
        if node is not None:
            return node.reward / node.visits
        else:
            return 0


    def _index_to_action(self, index):
        return index - 1


class BotNode(PlayerNode):

    def get_child(self, probabilities = None):
        best_child = max(self.children, key = self._node_UCT)
        if best_child is not None:
            return (best_child, False)
        else:
            return (self._create_child(self.children.index(None)), True)


class OpponentNode(PlayerNode):

    def get_child(self, probabilities):
        index = np_rand.choice(range(0,3), p=probabilities)

        if self.children[index] is not None:
            return (self.children[index], False)
        else:
            return (self._create_child(index), True)


#TODO: when stage is over but game is not over, avoid generating extra cardnodes
class CardNode(TreeNode):

    def __init__(self, game_state, our_seat):
        self.children = {}
        super.__init__(game_state, our_seat) 

    def get_child(self, probabilities = None):
        card_provider = self.state.card_provider.copy()
        card_provider.shuffle()

        index = None
        if self.state.stage == 0:
            index = get_cards_id(card_provider.peek_cards(3))
        else:
            index = get_cards_id(card_provider.peek_cards(1))

        if self.children.get(index) is None:
            new_node = _create_new_node(self) 
            new_node.state.card_provider = card_provider
            new_node.state.next_stage()
            new_node.state.deal_board()
            self.children[index] = new_node
            return (new_node, True)
        else:
            return (self.children[index], False)


    def perform(self, action_int):
        raise RuntimeError("CardNode state shouldn't be altered!")


    @property
    def actions(self):
        raise RuntimeError("CardNode shouldn't return actions!")


def get_reward(game_state, seat):
    our_player = game_state.table[seat]

    winners = game_state.get_winners()

    if our_player in winners:
        return game_state.pot / len(winners)
    else:
        return (our_player.chips_bet + our_player._total_chips_bet) * -1


def get_cards_id(cards):
    """Return a number which identifies the list of cards passed as argument."""
    return Card.prime_product_from_hand(Card.new(c) for c in cards)
