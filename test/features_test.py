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


    def test_get_features(self):
        feature_map = features.get_features(self.game)
        assert len(features.functions) == len(feature_map.keys())
