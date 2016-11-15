
class Seat:

    def __init__ (self, name = '', chips = 0):
        self.chips_bet = 0
        self.hand = []
        self.name = name
        self.chips = chips
        self._active = False
        self.reset()


    def place_bet(self, amount):
        self.chips -= amount
        self.chips_bet += amount


    def reset(self):
        bet = self.chips_bet
        self.chips_bet = 0

        if not self.empty and self.chips > 0:
            self._active = True
        else:
            self._active = False

        return bet


    def fold(self):
        self._active = False


    @property
    def empty(self):
        return self.name == ''

    @property
    def active(self):
        return not self.empty and self._active



class Table:

    def __init__ (self):
        self.seats = [Seat()] * 10 #table size
        self.current_seat = 0
        self.button_seat = 0
        self.board = []


    def __getitem__(self, index):
        return self.seats[index]


    def __setitem__(self, key, value):
        self.seats[key] = value


    def nextSeatIndex(self, seatIndex, neighbor = 1):
        """Returns the next active seat index given a seat number. Doesn't
        check whether there are active players at the table."""

        nextIndex = seatIndex

        while neighbor > 0:
            nextIndex = (nextIndex + 1) % 10
            seat = self.seats[nextIndex]
            if (not seat.empty) and seat.active:
                neighbor -= 1
        return nextIndex


    def new_round(self, start_from = None):
        map(lambda x: x.reset(), self.seats)

        if start_from == None:
            self.button_seat = self.nextSeatIndex(0)
        elif not self[start_from].empty:
            self.button_seat = start_from
        else:
            raise RuntimeError('Invalid starting seat!')

        self.current_seat = self.nextSeatIndex(self.button_seat, 3)


    def activePlayersOrdered(self):
        players = self[self.button_seat:] + self[:self.button_seat]

        return [p for p in players if p.active]


    def moveButton(self):
        self.button_seat = self.nextSeatIndex(self.button_seat)


    def nextPlayer(self):
        self.current_seat = self.nextSeatIndex(self.current_seat)


class GameState:

    def __init__ (self, big_blind = 1):
        self.stage = 0
        self.pot = 0
        self.raise_count = 0
        self.table = Table()
        self.big_blind = big_blind
        self.to_call = big_blind


    def new_game(self, start_from = None): #last seat index
        self.table.new_round(start_from)
        self.pot = 0
        self.raise_count = 0
        self.to_call = self.big_blind
        self._postBlinds()


    def _player_call(self, player):
        called = self.to_call - player.chips_bet
        player.place_bet(called)
        self.pot += called


    def _player_bet(self, player, bet):
        player.place_bet(bet)

        self.to_call += bet
        self.pot += bet
        self.raise_count += 1


    @property
    def current_bet_size(self):
        return self.big_blind if self.stage < 3 else self.big_blind * 2


    def fold(self):
        player = self.table[self.table.current_seat]
        player.fold()
        self.table.nextPlayer()

        if self.stage_over():
            self.next_stage()


    def call(self):
        player = self.table[self.table.current_seat]

        if player.chips_bet < self.to_call:
            self._player_call(player)

        self.table.nextPlayer()

        if self.stage_over():
            self.next_stage()


    def bet(self):
        player = self.table[self.table.current_seat]

        if player.chips_bet < self.to_call:
            self._player_call(player)

        self._player_bet(player, self.current_bet_size)

        self.table.nextPlayer()


    def _postBlinds(self): #TODO - for 2 players
        button_seat = self.table.button_seat

        sb_seat = self.table.nextSeatIndex(button_seat, 1)
        bb_seat = self.table.nextSeatIndex(button_seat, 2)

        self.table[sb_seat].place_bet(self.big_blind / 2)
        self.table[bb_seat].place_bet(self.big_blind)

        self.pot += self.big_blind * 1.5


    def _next_stage(self):
        self.stage += 1
        self.to_call = 0
        self.table.new_round(self.table.button_seat)


    def stage_over(self):
        return False


    def reward(self, parent, action):
        pass


    def is_terminal(self):
        pass


    def is_big_blind(self):
        pass


    def __eq__(self):
        pass


    def __hash__(self):
        pass


