from pokerbot.game_model import Table
from pokerbot.game_model import Seat

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


class TestSeat():

    def setup_method(self):
        self.seat = Seat('Blaine', 50)

    def test_bet(self):
        self.seat.bet(40)
        assert self.seat.chips == 10
        assert self.seat.chips_bet == 40
        assert self.seat.bet_count == 1

    def test_reset(self):
        self.seat.bet(10)
        self.seat.reset()
        assert self.seat.chips_bet == 0
        assert self.seat.bet_count == 0
        assert self.seat.active == True
