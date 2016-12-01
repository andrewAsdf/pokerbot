import pytest

from pokerbot.game_model import Table
from pokerbot.game_model import Seat
from pokerbot.game_model import GameState


class MockCardProvider:
    def __init__(self):
        self.hands = ['7s', '6s', '5s', '4s', '3s', '2s']

    def get_hand(self):
        return [self.hands.pop(), self.hands.pop()]

    def get_flop(self):
        return ['8s', '9s', 'Ts']

    def get_turn(self):
        return 'Js'

    def get_river(self):
        return 'Qs'


class TestSeat():

    def setup_method(self):
        self.seat = Seat('Blaine', 50)

    def test_bet(self):
        self.seat.place_bet(40)

        assert self.seat.chips == 10
        assert self.seat.chips_bet == 40

    def test_new_game(self):
        self.seat.place_bet(10)
        self.seat.new_game()

        assert self.seat.chips_bet == 0
        assert self.seat.active == True

    def test_empty(self):
        self.seat = Seat()
        assert self.seat.empty


    def test_fold(self):
        self.seat.fold()
        assert not self.seat.active


class TestTable():

    def setup_method(self):
        self.table = Table()
        self.table[1] = Seat('Andy', 40) #button
        self.table[5] = Seat('Blaine', 100)
        self.table[8] = Seat('Carly', 120)


    def test_constructor(self):
        assert self.table[1].name == 'Andy'
        assert self.table[1].chips == 40
        assert self.table[1].active == True
        assert self.table[1].empty == False


    def test_next_seat_index(self):
        assert self.table.next_index(0) == 1
        assert self.table.next_index(1, 1) == 5
        assert self.table.next_index(8, 2) == 5
        assert self.table.next_index(1, 3) == 1


    def test_move_button(self):
        self.table.move_button()
        assert self.table.button_index == 1


    def test_new_game(self):
        self.table.new_game(1)
        button_index = self.table.button_index

        assert button_index == 1

        assert self.table.current_index == 1
        #there are 3 players so button speaks first on the preflop


    def test_active_players_ordered(self):
        self.table.new_game(5)

        l = self.table.active_players_ordered()

        assert len(l) == 3

        assert l[0].name == 'Blaine'
        assert l[1].name == 'Carly'
        assert l[2].name == 'Andy'


    def test_active_players_orderedFoldedButton(self):
        self.table.new_game(5)
        self.table[5].fold()

        l = self.table.active_players_ordered()

        assert len(l) == 2

        assert l[0].name == 'Carly'
        assert l[1].name == 'Andy'


    def test_active_player_count(self):
        self.table.new_game(5)

        assert self.table.active_player_count == 3


class TestGameState:

    def setup_method(self):
        self.game = GameState(auto_stage = True)
        self.game.table[1] = Seat('Andy', 100)
        self.game.table[5] = Seat('Blaine', 100)
        self.game.table[8] = Seat('Carly', 100)
        self.game.new_game()


    def test_new_game(self):
        assert self.game.table[5].chips_bet == 0.5
        assert self.game.table[8].chips_bet == 1
        assert self.game.pot == 1.5


    def test_new_game_indexed(self):
        self.game.new_game(5)
        assert self.game.table[8].chips_bet == 0.5
        assert self.game.table[1].chips_bet == 1
        assert self.game.pot == 1.5


    def test_call(self):
        self.game.call() #Andy

        assert self.game.table[1].chips_bet == 1
        assert self.game.to_call == 1
        assert self.game.table.current_index == 5
        assert self.game.pot == 2.5


    def test_bet(self):
        self.game.bet() #Andy

        assert self.game.to_call == 2
        assert self.game.table[1].chips_bet == 2
        assert self.game.table.current_index == 5
        assert self.game.pot == 3.5

        self.game.bet() #Andy

        assert self.game.to_call == 3
        assert self.game.table[5].chips_bet == 3
        assert self.game.table.current_index == 8
        assert self.game.pot == 6


    def test_bet_call(self):
        self.game.bet() #Andy
        self.game.call() #Blaine

        assert self.game.to_call == 2
        assert self.game.pot == 5
        assert self.game.table[1].chips_bet == 2


    def test_fold(self):
        self.game.fold() #Andy
        self.game.call() #Blaine

        assert self.game.table.current_index == 8
        assert self.game.stage == 0
        assert self.game.pot == 2
        assert self.game.to_call == 1


    def test_new_stage(self):
        self.game.call() #Andy
        self.game.call() #Blaine
        self.game.call() #Carly

        assert self.game.pot == 3
        assert self.game.to_call == 0
        assert self.game.stage == 1

        assert self.game.table.current_index == 5
        assert self.game.table[5].chips == 99
        assert self.game.table[5].chips_bet == 0


    def test_new_stage_fold(self):
        self.game.fold() #Andy
        self.game.call() #Blaine
        self.game.call() #Carly

        assert self.game.stage == 1
        assert not self.game.table[1].active

        self.game.call() #Blaine
        self.game.call() #Carly

        assert self.game.stage == 2


    def test_new_stage_fold_after_button(self):
        self.game.call() #Andy
        self.game.fold() #Blaine
        self.game.call() #Carly

        assert self.game.stage == 1
        assert not self.game.table[5].active

        self.game.call() #Carly
        self.game.call() #Andy

        assert self.game.stage == 2


    def test_turn_and_river_bet(self):
        assert self.game.table.current_seat.name == 'Andy'
        self.game.call() #Andy
        assert self.game.table.current_seat.name == 'Blaine'
        self.game.call() #Blaine
        assert self.game.table.current_seat.name == 'Carly'
        self.game.call() #Carly

        assert self.game.table.current_seat.name == 'Blaine'
        self.game.call() #Blaine
        assert self.game.table.current_seat.name == 'Carly'
        self.game.call() #Carly
        assert self.game.table.current_seat.name == 'Andy'
        self.game.call() #Andy

        assert self.game.table.current_seat.name == 'Blaine'
        self.game.bet() #Blaine

        assert self.game.table[5].chips_bet == 2 #on the turn bet is 2BB
        assert self.game.table[5].chips == 97
        assert self.game.pot == 5


    def test_game_over(self):
        self.game.call() #Andy
        self.game.call() #Blaine
        self.game.call() #Carly

        self.game.call() #Blaine
        self.game.call() #Carly
        self.game.call() #Andy

        self.game.call() #Blaine
        self.game.call() #Carly
        self.game.call() #Andy

        self.game.call() #Blaine
        self.game.call() #Carly
        self.game.call() #Andy

        assert self.game.is_over()


    def test_game_over_fold(self):
        self.game.fold() #Andy
        self.game.fold() #Blaine

        assert self.game.is_over()


    def test_pot_multiple_stages(self):
        self.game.call() #Andy
        self.game.call() #Blaine
        self.game.bet()  #Carly
        self.game.call() #Andy
        self.game.call() #Blaine

        #Andy:   $2
        #Blaine: $2
        #Carly:  $2

        assert self.game.pot == 6

        self.game.call() #Blaine
        self.game.bet() #Carly
        self.game.fold() #Andy
        self.game.call() #Blaine

        #Andy:   $3
        #Blaine: $3
        #Carly:  $2 #fold

        assert self.game.pot == 8


    def test_card_provider(self):
        self.game.card_provider = MockCardProvider()
        self.game.new_game()

        assert self.game.table[1].hand == ['2s', '3s']
        assert self.game.table[5].hand == ['4s', '5s']
        assert self.game.table[8].hand == ['6s', '7s']

        self.game.call() #Andy
        self.game.call() #Blaine
        self.game.call() #Carly

        assert self.game.table.board == ['8s', '9s', 'Ts']

        self.game.call() #Blaine
        self.game.call() #Carly
        self.game.call() #Andy

        assert self.game.table.board == ['8s', '9s', 'Ts', 'Js']

        self.game.call() #Blaine
        self.game.call() #Carly
        self.game.call() #Andy

        assert self.game.table.board == ['8s', '9s', 'Ts', 'Js', 'Qs']


    def test_get_winner(self):
        self.game.table.board = ['8s', '9s', 'Ts', 'Jd', 'Qd']

        self.game.table[1].hand = ['2s', '3s']
        self.game.table[5].hand = ['4s', '5s']
        self.game.table[8].hand = ['6s', '7s']

        assert self.game.get_winners() == [self.game.table[8]]
