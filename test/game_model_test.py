from pokerbot.game_model import Table
from pokerbot.game_model import Seat
from pokerbot.game_model import GameState

class TestSeat():

    def setup_method(self):
        self.seat = Seat('Blaine', 50)

    def test_bet(self):
        self.seat.place_bet(40)

        assert self.seat.chips == 10
        assert self.seat.chips_bet == 40

    def test_reset(self):
        self.seat.place_bet(10)
        self.seat.reset()

        assert self.seat.chips_bet == 0
        assert self.seat.active == True


class TestTable():

    def setup_method(self):
        self.table = Table()
        self.table[1] = Seat('Andy', 40)
        self.table[5] = Seat('Blaine', 100)
        self.table[8] = Seat('Carly', 120)


    def test_constructor(self):
        assert self.table[1].name == 'Andy'
        assert self.table[1].chips == 40


    def test_nextSeatIndex(self):
        assert self.table.nextSeatIndex(0) == 1
        assert self.table.nextSeatIndex(1, 1) == 5
        assert self.table.nextSeatIndex(8, 2) == 5
        assert self.table.nextSeatIndex(1, 3) == 1


    def test_moveButton(self):
        self.table.moveButton()
        assert self.table.button_seat == 1


    def test_newGame(self):
        self.table.new_game()
        button_seat = self.table.button_seat

        assert button_seat == 1

        small_blind = self.table.nextSeatIndex(button_seat, 1)
        big_blind = self.table.nextSeatIndex(button_seat, 2)

        assert self.table.current_seat == 1


    def test_newGameIndexed(self):
        self.table.new_game(1)

        assert self.table.button_seat == 5
        assert self.table.current_seat == 5


class TestGameState:

    def setup_method(self):
        self.game = GameState()
        self.game.table[1] = Seat('Andy', 40)
        self.game.table[5] = Seat('Blaine', 100)
        self.game.table[8] = Seat('Carly', 120)
        self.game.new_game()


    def test_new_game(self):
        assert self.game.table[5].chips_bet == 0.5
        assert self.game.table[8].chips_bet == 1
        assert self.game.pot == 1.5


    def test_call(self):
        self.game.call()

        assert self.game.table[1].chips_bet == 1
        assert self.game.to_call == 1
        assert self.game.table.current_seat == 5
        assert self.game.pot == 2.5


    def test_bet(self):
        self.game.bet()

        assert self.game.to_call == 2
        assert self.game.table[1].chips_bet == 2
        assert self.game.raise_count == 1
        assert self.game.table.current_seat == 5
        assert self.game.pot == 3.5

        self.game.bet()

        assert self.game.to_call == 3
        assert self.game.table[5].chips_bet == 3
        assert self.game.raise_count == 2
        assert self.game.table.current_seat == 8
        assert self.game.pot == 6


    def test_bet_call(self):
        self.game.bet()
        self.game.call()

        assert self.game.to_call == 2
        assert self.game.pot == 5
        assert self.game.table[1].chips_bet == 2
