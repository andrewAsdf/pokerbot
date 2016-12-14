from deuces import Card
import math
import logging
from itertools import accumulate
import random

logger = logging.getLogger('pokerbot.decision_maker')


class MCTSDecisionMaker:

    def __init__(self, opponent_modeller, db, card_provider):
        self.opponent_modeller = opponent_modeller
        self.db = db
        self.card_provider = card_provider


    def get_action(self, game_state, max_iter=2000):
        assert game_state.auto_deal == False
        logger.info('MCTS iteration count: {}'.format(max_iter))

        names = (s.name for s in game_state.table.seats if s.active)
        self.vpips = self._get_player_vpips(names)

        our_seat = game_state.table.current_index
        self.root = self._create_root(game_state, our_seat)

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
        while not is_new and not node.has_reward():
            node, is_new = node.get_child(self._get_probabilities(node))
        return node


    def _simulate(self, node):
        simulation_node = PlayerNode(node.state.copy(), node.our_seat) #card nodes would behave
        simulation_node.state.auto_stage = True                 #differently
        simulation_node.state.auto_deal = True
        simulation_node.state.card_provider.shuffle()

        if simulation_node.state.stage_over():
            simulation_node.state.next_stage()

        while not simulation_node.has_reward():
            if simulation_node.our_turn():
                choice = random.choice(simulation_node.actions) #TODO: apply an OM instead
                perform(simulation_node.state, choice)
            else:
                prediction = self._get_prediction(simulation_node)
                perform(simulation_node.state, prediction)

        self._fill_player_cards(simulation_node)

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
        return probabilities


    def _assign_card_provider(self, node):
        self.card_provider.reset()
        self.card_provider.shuffle()

        our_cards = node.state.table[node.our_seat].hand
        board_cards = node.state.table.board

        self.card_provider.remove_cards(our_cards + board_cards)
        node.state.card_provider = self.card_provider.copy()


    def _fill_player_cards(self, node):
        seats = node.state.table.seats
        for seat in (s for i, s in enumerate(seats) if s.active and i != node.our_seat):
            vpip = 1 if self.vpips[seat.name] else self.vpips[seat.name]
            hand = node.state.card_provider.get_hand(vpip = vpip)
            seat.hand = hand


    def _get_player_vpips(self, player_names):
        return {p : self.db.get_player_stat(p, 'vpip') for p in player_names}


    def _create_root(self, game_state, our_seat):
        root = BotNode(game_state.copy(), our_seat)
        root.state.auto_stage = False
        root.visits = 1
        self._assign_card_provider(root)
        return root


class TreeNode:

    def __init__(self, game_state, our_seat):
        self.parent = None
        self.visits = 0
        self.reward = 0

        self.state = game_state
        self.our_seat = our_seat


    def get_reward(self):
        assert self.has_reward(), 'Cannot get reward yet!'
        return get_reward(self.state, self.our_seat)


    def _node_UCT(self, node):
        if node is None:
            return 5 * math.sqrt(math.log(self.visits))
        else:
            n = node.visits
            r = node.reward
            return r / n + 5 * math.sqrt(math.log(self.visits) / n)


    def our_turn(self):
        return self.state.table.current_index == self.our_seat


    def has_reward(self): #reward is known when we fold, even if game is going
        return self.state.is_over() or not self.state.table[self.our_seat].active


    def stage_over(self):
        return self.state.stage_over()


    _player_actions = [-1, 0, 1]
    _player_actions_noraise = [-1, 0]

    @property
    def actions(self):
        if self.state.possible_to_raise():
            return self._player_actions
        else:
            return self._player_actions_noraise



def _child_value(node):
    if node is not None:
        return node.reward / node.visits
    else:
        return 0


class PlayerNode(TreeNode):

    def __init__(self, game_state, our_seat):
        self.children = [None, None, None]
        super().__init__(game_state, our_seat)


    def _create_child(self, index):
        new_state = self.state.copy()
        perform(new_state, self._index_to_action(index))
        new_node = _create_new_node(new_state, self.our_seat)
        new_node.parent = self
        self.children[index] = new_node
        return new_node


    def get_best_action(self):
        best_child = max(self.children, key=_child_value)
        index = self.children.index(best_child)
        return self._index_to_action(index)


    def _index_to_action(self, index):
        return index - 1


class BotNode(PlayerNode):

    def get_child(self, probabilities = None):
        assert not self.state.stage_over()

        best_child = None
        if self.state.possible_to_raise():
            best_child = max(self.children, key = self._node_UCT)
        else:
            best_child = max(self.children[0:2], key = self._node_UCT)

        if best_child is not None:
            return (best_child, False)
        else:
            return (self._create_child(self.children.index(None)), True)
            #TODO: it will always choose the same index first


class OpponentNode(PlayerNode):

    def get_child(self, probabilities):
        assert not self.state.stage_over()

        index = 0
        if self.state.possible_to_raise():
            index = pick_index(probabilities)
        else:
            index = pick_index(probabilities[0:2])

        if self.children[index] is not None:
            return (self.children[index], False)
        else:
            return (self._create_child(index), True)


class CardNode(TreeNode):

    def __init__(self, game_state, our_seat):
        self.children = {}
        super().__init__(game_state, our_seat)

    def get_child(self, probabilities = None):
        assert self.state.stage_over()
        card_provider = self.state.card_provider.copy()
        card_provider.shuffle()

        index = None
        if self.state.stage == 0:
            index = get_cards_id(card_provider.peek_cards(3))
        else:
            index = get_cards_id(card_provider.peek_cards(1))

        if self.children.get(index) is None:
            new_state = self.state.copy()
            new_state.card_provider = card_provider
            new_state.next_stage()
            new_state.deal_board()
            new_node = _create_new_node(new_state, self.our_seat)
            new_node.parent = self
            self.children[index] = new_node
            return (new_node, True)
        else:
            return (self.children[index], False)


def _create_new_node(game_state, our_seat):
    '''Create a new node using the state found in node.'''

    if game_state.stage_over():
        return CardNode(game_state, our_seat)

    elif game_state.table.current_index == our_seat:
        return BotNode(game_state, our_seat)

    else:
        return OpponentNode(game_state, our_seat)


def perform(game_state, action_int):
    if action_int == 1:
        game_state.bet()
    elif action_int == 0:
        game_state.call()
    elif action_int == -1:
        game_state.fold()
    else:
        raise RuntimeError('Invalid action to perform!')


def get_reward(game_state, seat):
    our_player = game_state.table[seat]

    if not our_player.active:
        return (our_player.chips_bet + our_player._total_chips_bet) * -1

    winners = game_state.get_winners()

    if our_player in winners:
        return game_state.pot / len(winners)
    else:
        return (our_player.chips_bet + our_player._total_chips_bet) * -1


def get_cards_id(cards):
    """Return a number which identifies the list of cards passed as argument."""
    return Card.prime_product_from_hand(Card.new(c) for c in cards)


def pick_index(probabilities):
    limits = list(accumulate(probabilities))
    choice = random.uniform(0, limits[-1])
    return next(i for i, l in  enumerate(limits) if choice < l)


def _node_balance(node):
    if node is None:
        return 1
    return 1 / node.visits

