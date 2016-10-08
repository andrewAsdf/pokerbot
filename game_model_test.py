import pytest

from game_model import Table
from game_model import Seat

class TestTable():

    def setup_method(self):
        self.table = Table()
        self.table[1] = Seat('Andy', 40)
        self.table[5] = Seat('Blaine', 100)
        self.table[8] = Seat('Carly', 120)


    def test_constructor(self):
        assert self.table[1].name == 'Andy'
        assert self.table[1].stack == 40


    def test_nextSeatIndex(self):
        assert self.table.nextSeatIndex(0) == 1
        assert self.table.nextSeatIndex(1) == 5
        assert self.table.nextSeatIndex(8) == 1
