import enum


class Seat:

    def __init__ (self, name = '', chips = 0):
        self.name = name
        self.chips = chips
        self.chips_bet = 0
        self.hand = []
        self.active = True


    def place_bet(self, amount):
        self.chips -= amount
        self.chips_bet += amount


    def reset(self):
        self.chips_bet = 0
        self.active = True if self.chips > 0 else False


    def fold(self):
        self.active = False


    @property
    def empty(self):
        return True if self.name == '' else False



class Table:

    def __init__ (self):
        self.seats = [Seat()] * 10
        self.current_seat = 0
        self.button_seat = 0
        self.board = []


    def __getitem__(self, index):
        return self.seats[index]


    def __setitem__(self, key, value):
        self.seats[key] = value


    def nextSeatIndex(self, seatIndex, neighbor = 1):

        nextIndex = seatIndex

        while neighbor > 0:
            nextIndex = (nextIndex + 1) % 10
            seat = self.seats[nextIndex]
            if (not seat.empty) and seat.active:
                neighbor -= 1

        return nextIndex


    def clear(self):
        self = Table()


    def new_game(self, start_from = 9):
        map(lambda x: x.reset(), self.seats)

        self.button_seat = self.nextSeatIndex(start_from)
        self.current_seat = self.nextSeatIndex(self.button_seat, 3)


    def moveButton(self):
        self.button_seat = self.nextSeatIndex(self.button_seat)

    def nextPlayer(self):
        self.current_seat = self.nextSeatIndex(self.current_seat)


class GameState:

    def __init__ (self, big_blind = 1):
        self.stage = 1
        self.table = Table()
        self.actions = []
        self.pot = 0
        self.raise_count = 0
        self.big_blind = big_blind
        self.to_call = big_blind


    def new_game(self):
        self.table.new_game()
        self.to_call = self.big_blind
        self._postBlinds()


    def fold(self, seat_index = None):
        player = self.table[self.table.current_seat]
        player.fold()
        self.table.nextPlayer()

        if self.stage_over():
            self.next_stage()


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
    def current_bet(self):
        return self.big_blind if self.stage < 3 else self.big_blind * 2


    def call(self, seat_index = None):
        player = self.table[self.table.current_seat]

        if player.chips_bet < self.to_call:
            self._player_call(player)

        self.table.nextPlayer()

        if self.stage_over():
            self.next_stage()


    def bet(self, seat_index = None):
        player = self.table[self.table.current_seat]

        if player.chips_bet < self.to_call:
            self._player_call(player)

        self._player_bet(player, self.current_bet)

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


    def stage_over(self):
        return False


    def reward(self, parent, action):
        pass


    def is_terminal(self):
        pass


    def __eq__(self):
        pass


    def __hash__(self):
        pass


