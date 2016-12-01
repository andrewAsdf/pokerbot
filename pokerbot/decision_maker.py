from random import Random
import math
import logging

logger = logging.getLogger('pokerbot.decision_maker')


def get_reward(game_state, seat):
    our_player = game_state.table[seat]

    winners = game_state.get_winners()

    if our_player in winners:
        return game_state.pot / len(winners)
    else:
        return (our_player.chips_bet + our_player._total_chips_bet) * -1


class TreeNode:

    _player_actions = [-1, 0, 1]
    _player_actions_noraise = [-1, 0]

    def __init__(self, game_state, our_seat, random = Random()):
        self.parent = None
        self.children = [None, None, None]
        self.visits = 1
        self.reward = 0

        self.random = random
        self.state = game_state.copy()
        self.our_seat = our_seat


    def copy(self):
        return TreeNode(self.state, self.our_seat, self.random)


    def perform(self, action_int):
        if action_int == 1:
            self.state.bet()
        elif action_int == 0:
            self.state.call()
        elif action_int == -1:
            self.state.fold()
        else:
            raise RuntimeError('Invalid action to perform!')


    def get_reward(self):
        if not state.is_over():
            raise RuntimeError('Cannot get reward for running game!')
        return get_reward(self.state, self.our_seat)


    @property
    def actions(self):
        if self.state.possible_to_raise():
            return self._player_actions
        else:
            return self._player_actions_noraise


    def get_player_move_node(self):
        best_child = max(self.children, key = _node_UCT)
        if best_child is not None:
            return (best_child, False)
        else:
            return (_create_child(self.children.index(None)), True)


    def get_opponent_move_node(self, probabilities):
        index = next(p for p in probabilities if random.random() < p)

        if self.children[index] is not None:
            return (self.children[index], False)
        else:
            return (_create_child(index), True)


    def _create_child(self, index):
        self.children[index] = self.copy()
        self.children[index].perform(index - 1)

        if self.state.stage_over():
            self.children[index] = CardNode()

        new_node.parent = self
        new_node.perform(action_int)
        self.children.append(new_node)
        self._children_actions.append(action_int)

        return new_node


    def _node_UCT(node):
        if Node is none:
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


    def _child_value(self, node):
        if node is not None:
            return node.reward / node.visits
        else:
            return 1


    def get_best_action(self, key = self.child_value):
        best_child = max(self.children, key)
        index = self.children.index(best_child) + 1
        return _index_to_action(index)


    def _index_to_action(self, index):
        return index + 1



class CardNode(TreeNode):

    def __init__(self, node):
        super.__init__(node.state, node.our_seat, node.random)
        self.children = {}


    def get_player_move_node(self):
        return self.get_node()


    def get_opponent_move_node(self):
        return self.get_node()


    def get_node(self):
        new_node = self.copy()
        new_node.card_provider.shuffle()
        new_node.state.next_stage()
        board = new_node.state.table.board
        children(frozenset(board) : new_node)


class MCTSDecisionMaker:

    def __init__(self, opponent_modeller, db, card_provider, pseudo_random = False):
        self.opponent_modeller = opponent_modeller
        self.db = db
        self.random = Random(420) if pseudo_random else Random()
        self.card_provider = card_provider


    def get_action(self, game_state, max_iter=2000):
        logger.info('MCTS iteration count: {}'.format(max_iter))
        our_seat = game_state.table.current_index
        logger.info('Getting decision for player {}'
                .format(game_state.table.current_seat.name))

        self.root = TreeNode(game_state, our_seat)
        self._assign_card_provider(self.root)

        for i in range(max_iter):
            if not (i + 1) % 500:
                logger.info('MCTS iteration: {}'.format(i + 1))
            self._do_iteration(self.root)

        action = self.root.get_best_action()
        logger.info('Chosen action: {}'.format(action))
        return action


    def _do_iteration(self, root):
        node, is_new = root.get_action_child()

        while not is_new:
            if node.is_terminal():
                node, is_new = (node, True) #quick solution for exiting loop
            elif node.stage_over():
                node, is_new = node.get_card_node()
            elif node.our_turn():
                node, is_new = node.get_player_move_node()
            else:
                node, is_new = node.get_opponent_move_node()

        reward = self._simulate(node)

        self._backpropagate(node, reward)


    def _simulate(self, node):
        simulation_node = node.copy()
        simulation_node.state.card_provider.shuffle()

        while not simulation_node.is_terminal():
            if simulation_node.our_turn():
                choice = self.random.choice(simulation_node.actions)
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


    def _assign_card_provider(self, node):
        our_cards = node.state.table[node.our_seat].hand
        board_cards = node.state.table.board
        self.card_provider.remove_cards(our_cards + board_cards)
        self.card_provider.shuffle()
        node.state.card_provider = self.card_provider
