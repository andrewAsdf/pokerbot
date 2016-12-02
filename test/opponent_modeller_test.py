from pokerbot.opponent_modeller import OpponentModeller
import pokerbot.features as features
import pokerbot.stats as stats


test_game = {
        "_id" : 999,
        "actions" : [
                {
                        "seat" : 3,
                        "amount" : 0.5,
                        "type" : "smallBlind"
                },
                {
                        "seat" : 4,
                        "amount" : 1.0,
                        "type" : "bigBlind"
                },
                {
                        "seat" : 5,
                        "type" : "call"
                },
                {
                        "seat" : 1,
                        "type" : "call"
                },
                {
                        "seat" : 2,
                        "type" : "fold"
                },
                {
                        "seat" : 3,
                        "type" : "call"
                },
                {
                        "seat" : 4,
                        "type" : "check"
                },
                {
                        "stage" : "flop",
                        "cards" : [
                                "5s",
                                "7c",
                                "Kh"
                        ],
                        "type" : "board"
                },
                {
                        "seat" : 3,
                        "type" : "check"
                },
                {
                        "seat" : 4,
                        "type" : "check"
                },
                {
                        "seat" : 5,
                        "type" : "check"
                },
                {
                        "seat" : 1,
                        "type" : "check"
                },
                {
                        "stage" : "turn",
                        "cards" : [
                                "5s",
                                "7c",
                                "Kh",
                                "Ac"
                        ],
                        "type" : "board"
                },
                {
                        "seat" : 3,
                        "amount" : 2.0,
                        "type" : "bet"
                },
                {
                        "seat" : 4,
                        "type" : "fold"
                },
                {
                        "seat" : 5,
                        "type" : "call"
                },
                {
                        "seat" : 1,
                        "type" : "fold"
                },
                {
                        "stage" : "river",
                        "cards" : [
                                "5s",
                                "7c",
                                "Kh",
                                "Ac",
                                "3s"
                        ],
                        "type" : "board"
                },
                {
                        "seat" : 3,
                        "amount" : 2.0,
                        "type" : "bet"
                },
                {
                        "seat" : 5,
                        "type" : "call"
                },
                {
                        "wins" : {
                                3 : 12.0
                        },
                        "type" : "gameover"
                }
        ],
        "table" : [
                {
                        "name" : "Jagbot",
                        "hand" : [ ],
                        "seat_number" : 1,
                        "stack" : 100
                },
                {
                        "name" : "Jagger",
                        "hand" : [ ],
                        "seat_number" : 2,
                        "stack" : 100
                },
                {
                        "name" : "Lionel",
                        "hand" : [ ],
                        "seat_number" : 3,
                        "stack" : 100
                },
                {
                        "name" : "Malory",
                        "hand" : [ ],
                        "seat_number" : 4,
                        "stack" : 100
                },
                {
                        "name" : "MyBot",
                        "hand" : [ ],
                        "seat_number" : 5,
                        "stack" : 100
                }
        ],
        "button" : 2
}


class MockDB:

    def __init__(self):
        self.last_processed_game = 1
        self.player_models = {}
        self.player_stats = {}


    def get_games(self):
        return [test_game]


    def add_player_model(self, name, model):
        self.player_models[name] = model


    def get_player_model(self, name):
        if (self.player_models.get(name) == None):
            return None
        else:
            return self.player_models[name]


    def add_player_features(self, name, inputs, answers):
        pass


    def add_player_stat(self, name, stat, value):
        if self.player_stats.get(name) is None:
            self.player_stats[name] = {}

        self.player_stats[name][stat] = value


    @property
    def unprocessed_game_count(self):
        return 0



class MockModelCreator:

    def __init__(self):
        self.feature_matrices = {}


    def make_model(self, inputs, answers, prev_model):
        return inputs, answers


    def use_model(self, model, features):
        return 1


class MockStatCreator:
    pass


class TestOpponentModeller:

    def setup_method(self):
        model_creator = MockModelCreator()
        stat_creator = MockStatCreator()
        self.opp_mod = OpponentModeller(features.functions, MockDB(), 1, model_creator, stats.functions)


    def test_create_game_state(self):
        button = test_game['button']
        table_data = test_game['table']
        game = self.opp_mod.create_game_state(table_data, button)

        assert len(game.table.active_players_ordered()) == 5
        assert game.table[1].name == 'Jagbot'
        assert game.table[5].name == 'MyBot'

        assert game.table[1].chips == 100
        assert game.table[2].chips == 100 #button
        assert game.table[3].chips == 99.5
        assert game.table[4].chips == 99
        assert game.table[5].chips == 100


    def test_get_features(self):
        features = self.opp_mod.get_features(test_game)
        assert len(features.keys()) == 5

        assert len(features['MyBot']) == 4
        assert len(features['Jagbot']) == 3

        assert len(features['MyBot'][0]) == 2 #they should be tuples


    def test_process_stats(self):
        self.opp_mod.process_stats([test_game])

        assert self.opp_mod.db.player_stats['Jagbot']['vpip'] == 1
        # An actual stat is used here for testing purposes


    def test_process_games(self):
        self.opp_mod.process_games()

        assert len(self.opp_mod.db.get_player_model('MyBot')[0]) == 4
        assert len(self.opp_mod.db.get_player_model('MyBot')[1]) == 4
        # MockModelCreator returns the original input tuple,
        # and MockDB stores it.
        assert self.opp_mod.db.get_player_model('MyBot')[1][0] == 0
        assert self.opp_mod.db.get_player_model('MyBot')[1][1] == 0
        assert self.opp_mod.db.get_player_model('MyBot')[1][2] == 0
        assert self.opp_mod.db.get_player_model('MyBot')[1][3] == 0
        # The second tuple contains ints for the player's actions


    def test_get_prediction(self):
        button = test_game['button']
        table_data = test_game['table']
        game = self.opp_mod.create_game_state(table_data, button)

        assert self.opp_mod.get_prediction(game) == 0

        self.opp_mod.process_games()

        assert self.opp_mod.get_prediction(game) == 1

