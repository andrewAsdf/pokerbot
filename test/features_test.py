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

# Andy:   2$
# Blaine: 3$
# Carly:  1$ - has to call 2$

        assert features.pot_odds(self.game) == 2 / (2 + 6)
