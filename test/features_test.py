import pokerbot.features as features
from pokerbot.game_model import GameState
from pokerbot.game_model import Seat

class TestFeatures:

    def setup_method(self):
        self.game = GameState()
        self.game.table[1] = Seat('Andy', 40)
        self.game.table[5] = Seat('Blaine', 100)
        self.game.table[8] = Seat('Carly', 120)
        self.game.new_game()

    def test_raise_count(self):
        self.game.bet()
        self.game.bet()

        assert features.raise_count(self.game) == 2


    def test_pot_odds(self):
        self.game.bet()
        self.game.bet()

        assert features.pot_odds(self.game) == 2 / (2 + 6)

        # Andy:   2$
        # Blaine: 3$
        # Carly:  1$ - has to call 2$


    def test_position(self):
        assert features.position(self.game) == 3/3

        self.game.call()
        assert features.position(self.game) == 2/3

        self.game.call()
        assert features.position(self.game) == 1/3


    def test_position_with_moved_button(self):
        self.game.new_game(5)

        assert features.position(self.game) == 3/3


    def test_bets_to_call(self):
        self.game.bet()
        self.game.bet()

        assert features.bets_to_call(self.game) == 2


    def test_committed(self):
        """Blinds should count as committed chips"""
        assert features.committed(self.game) == False

        self.game.call()

        assert features.committed(self.game) == True


    def test_board_card_rank(self):
        self.game.table.board = ['Ad', 'Kc', 'Qd']
        assert features.first_card_rank(self.game) == 13 / 13
        assert features.second_card_rank(self.game) == 12 / 13
        assert features.third_card_rank(self.game) == 11 / 13
        assert features.fourth_card_rank(self.game) == 0


    def test_card_on_board(self):
        self.game.table.board = ['Ad', 'Tc', '9d']
        assert features.ace_on_board(self.game)
        assert not features.king_on_board(self.game)

