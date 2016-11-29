from random import Random
import math
import logging

logger = logging.getLogger('pokerbot.decision_maker')

class TreeNode:

    _actions = [-1, 0, 1]
    _actions_noraise = [-1, 0]

    def __init__(self, game_state, our_seat):
        self.parent = None
        self.children = []
        self._children_actions = []
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


    def get_reward(self):
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
            return self._actions
        else:
            return self._actions_noraise


    def copy(self):
        return TreeNode(self.state, self.our_seat)


    def create_child(self, action_int):
        new_node = TreeNode(self.state, self.our_seat)
        new_node.parent = self
        new_node.perform(action_int)
        self.children.append(new_node)
        self._children_actions.append(action_int)
        return new_node


    def our_turn(self):
        return self.state.table.current_index == self.our_seat


    def is_terminal(self):
        return self.state.is_over()


    def get_best_action(self):
        best_child =  max(self.children, key = lambda c: c.reward / c.visits)
        return next(action for action, node in
                zip(self._children_actions, self.children) if node == best_child)




def _node_UCT(node):
    n = node.visits
    r = node.reward
    t = node.parent.visits
    return r / n + 1.41 * math.sqrt(math.log(t) / n)


class MCTSDecisionMaker:

    def __init__(self, opponent_modeller, db, pseudo_random = False):
        self.opponent_modeller = opponent_modeller
        self.db = db
        self.random = Random(420) if pseudo_random else Random()


    def get_action(self, game_state, max_iter=2000):
        logger.info('MCTS iteration count: {}'.format(max_iter))
        our_seat = game_state.table.current_index
        logger.info('Getting decision for player {}'
                .format(game_state.table.current_seat.name))

        self.root = TreeNode(game_state, our_seat)

        for i in range(max_iter):
            if not (i + 1) % 500:
                logger.info('MCTS iteration: {}'.format(i + 1))
            selected_node = self._select(self.root)
            expanded_node = self._expand(selected_node)
            reward = self._simulate(expanded_node)
            self._backpropagate(expanded_node, reward)

        action = self.root.get_best_action()
        logger.info('Chosen action: {}'.format(action))
        return action


    def _select(self, node, strategy = _node_UCT):
        selected_node = node
        while selected_node.children:
            if len(selected_node.children) == 1:
                selected_node = selected_node.children[0]
            else:
                selected_node = max(selected_node.children, key = strategy)

        return selected_node


    def _expand(self, node):
        if (node.is_terminal()):
            return node

        if node.our_turn():
            for action in node.actions:
                node.create_child(action)
        else:
            prediction = self._get_prediction(node)
            node.create_child(prediction)

        return self.random.choice(node.children)


    def _simulate(self, node):
        simulation_node = node.copy()

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
