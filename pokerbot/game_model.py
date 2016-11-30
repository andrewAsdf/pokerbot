from deuces import Card
from deuces import Evaluator
from copy import copy


class Seat:

    def __init__ (self, name = '', chips = 0, hand = []):
        self.chips_bet = 0
        self.hand = hand
        self.name = name
        self.chips = chips
        self._folded = False
        self._total_chips_bet = 0 #TODO: hack for counting loss


    def place_bet(self, amount):
        self.chips -= amount
        self.chips_bet += amount
        self._total_chips_bet += amount


    def clear_bets(self):
        self.chips_bet = 0


    def fold(self):
        self._folded = True


    def new_game(self):
        self._folded = False
        self.chips_bet = 0
        self._total_chips_bet = 0


    def set_hand(self, hand):
        self.hand = hand


    @property
    def empty(self):
        return self.name == ''


    @property
    def active(self):
        return not self.empty and not self._folded



class Table:

    def __init__ (self):
        self.seats = [Seat()] * 10 #table size
        self.current_index = 0
        self.button_index = 0
        self.stop_index = 0
        self.board = []


    def copy(self):
        new_table = copy(self)
        new_table.board = copy(self.board)
        new_table.seats = [copy(s) for s in self.seats]
        return new_table


    def __getitem__(self, index):
        return self.seats[index]


    def __setitem__(self, key, value):
        self.seats[key] = value


    def next_index(self, seat_index, neighbor = 1):
        """Return the next active seat index given a seat number."""

        if self.active_player_count == 0:
            raise RuntimeError('Cannot get index for zero players!')

        next_index = seat_index

        while neighbor > 0:
            next_index = (next_index + 1) % 10
            seat = self.seats[next_index]
            if (not seat.empty) and seat.active:
                neighbor -= 1
        return next_index


    def new_game(self, start_from):
        [s.new_game() for s in self.seats]

        if start_from == None:
            self.button_index = self.next_index(0)
        elif not self[start_from].empty:
            self.button_index = start_from
        else:
            raise RuntimeError('Invalid starting seat!')

        self.current_index = self.next_index(self.button_index, 3)
        self.stop_index = self.next_index(self.button_index, 3)


    def next_stage(self):
        self.current_index = self.next_index(self.button_index, 1)
        self.stop_index = self.next_index(self.button_index, 1)


    def active_players(self):
        return [p for p in self.seats if p.active]


    def active_players_ordered(self):
        players = self[self.button_index:] + self[:self.button_index]
        return [p for p in players if p.active]


    @property
    def active_player_count(self):
        return sum(p.active for p in self.seats)


    def move_button(self):
        self.button_index = self.next_index(self.button_index)


    def next_seat(self):
        self.current_index = self.next_index(self.current_index)


    @property
    def current_seat(self):
        return self[self.current_index]


    @property
    def small_blind_seat(self):
        return self[self.next_index(self.button_index, 1)]


    @property
    def big_blind_seat(self):
        return self[self.next_index(self.button_index, 2)]


class GameState:

    evaluator = Evaluator()

    def __init__ (self, big_blind = 1, card_provider = None):
        self.card_provider = card_provider
        self.table = Table()
        self.stage = 0
        self._pot_previous_rounds = 0
        self.to_call = big_blind
        self.big_blind = big_blind
        self.bet_count = 0


    def copy(self):
        new_state = copy(self)
        new_state.table = self.table.copy()
        if self.card_provider is not None:
            new_state.card_provider = self.card_provider.copy()
        return new_state


    @property
    def current_bet_size(self): #preflop & flop: 1xBB, turn & river: 2xBB
        return self.big_blind if self.stage < 2 else self.big_blind * 2


    @property
    def pot(self):
        return self._pot_previous_rounds + self._current_round_pot


    @property
    def _current_round_pot(self):
        return sum([s.chips_bet for s in self.table.seats])


    @property
    def _bet_count(self):
        return self.to_call / self.big_blind


    def fold(self):
        player = self.table.current_seat
        player.fold()

        folding_player_index = self.table.current_index

        self.table.next_seat()

        if self.stage_over():
            self._next_stage()
        elif self.table.stop_index == folding_player_index:
            self.table.stop_index = self.table.next_index(folding_player_index)
            #if a player folds when first, next_index won't find it later so
            #stage would never end


    def call(self):
        player = self.table.current_seat

        if player.chips_bet < self.to_call:
            self._call(player)

        self.table.next_seat()

        if self.stage_over():
            self._next_stage()


    def bet(self):
        player = self.table.current_seat

        if player.chips_bet < self.to_call:
            self._call(player)

        self._bet(player, self.current_bet_size)

        self.table.stop_index = self.table.current_index
        self.table.next_seat()


    def new_game(self, start_from = None):
        self.table.new_game(start_from)

        if self.card_provider is not None:
            [p.set_hand(self.card_provider.get_hand())
                    for p in self.table.seats if p.active]

        self.to_call = self.big_blind
        self._pot_previous_rounds = 0
        self._postBlinds()


    def possible_to_raise(self):
        return self.bet_count < 4


    def _call(self, player):
        called = self.to_call - player.chips_bet
        player.place_bet(called)


    def _bet(self, player, bet):
        player.place_bet(bet)
        self.to_call += bet


    def _next_stage(self):
        self.stage += 1
        self.to_call = 0

        self._pot_previous_rounds += self._current_round_pot
        [s.clear_bets() for s in self.table.seats]

        if self.card_provider is not None:
            if self.stage == 1:
                self.table.board = self.card_provider.get_flop()
            elif self.stage == 2:
                self.table.board.append(self.card_provider.get_turn())
            elif self.stage == 3:
                self.table.board.append(self.card_provider.get_river())

        self.table.next_stage()


    def _postBlinds(self): #TODO - for 2 players
        self.table.small_blind_seat.place_bet(self.big_blind / 2)
        self.table.big_blind_seat.place_bet(self.big_blind)
        self.to_call = self.big_blind


    def stage_over(self):
        return self.table.current_index == self.table.stop_index


    def is_over(self):
        return self.table.active_player_count == 1 or self.stage == 4
        #stage will be incremented after river, so we check that


    def _evaluate_hand(self, ascii_cards):
        return self.evaluator.evaluate([Card.new(a) for a in ascii_cards],[])


    def get_winners(self):
        '''Return array of winner(s) of the game. No checking is performed whether game\
        is over.'''
        active = self.table.active_players()

        if len(active) == 1:
            return [active.pop()]

        if any(not p.hand for p in self.table.seats if p.active):
            [p.set_hand([]) for p in self.table.seats if (not p.hand) and p.active]

        hand_ranks = {p : self._evaluate_hand(p.hand + self.table.board) for p in active}
        winner_rank = min(hand_ranks.values()) #deuces uses small ranks for good hands

        return [p for p, rank in hand_ranks.items() if rank == winner_rank]
