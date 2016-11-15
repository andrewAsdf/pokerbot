from pokerbot.opponent_modeller import OpponentModeller
import pokerbot.features as features


test_game = {
        "_id" : 999,
        "actions" : [
                {
                        "seat" : "3",
                        "amount" : "0.5",
                        "type" : "smallBlind"
                },
                {
                        "seat" : "4",
                        "amount" : "1.0",
                        "type" : "bigBlind"
                },
                {
                        "seat" : "5",
                        "type" : "call"
                },
                {
                        "seat" : "1",
                        "type" : "call"
                },
                {
                        "seat" : "2",
                        "type" : "fold"
                },
                {
                        "seat" : "3",
                        "type" : "call"
                },
                {
                        "seat" : "4",
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
                        "seat" : "3",
                        "type" : "check"
                },
                {
                        "seat" : "4",
                        "type" : "check"
                },
                {
                        "seat" : "5",
                        "type" : "check"
                },
                {
                        "seat" : "1",
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
                        "seat" : "3",
                        "amount" : "2.0",
                        "type" : "bet"
                },
                {
                        "seat" : "4",
                        "type" : "fold"
                },
                {
                        "seat" : "5",
                        "type" : "call"
                },
                {
                        "seat" : "1",
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
                        "seat" : "3",
                        "amount" : "2.0",
                        "type" : "bet"
                },
                {
                        "seat" : "5",
                        "type" : "call"
                },
                {
                        "wins" : {
                                "3" : "12.0"
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


    def get_games(self, from_id):
        return [test_game]


    @property
    def unprocessed_game_count(self):
        return 0


class MockObservationProcessor():

    def __init__(self):
        self.observations = []


    def new_observation(self, features, action):
        self.observations.append((features, action))


class TestOpponentModeller:

    def setup_method(self):
        processor = MockObservationProcessor()
        self.opp_mod = OpponentModeller(features.functions, MockDB(), 1, processor)


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


    def test_replay_game(self):
        game = self.opp_mod.replay_game(test_game)

        assert len(self.opp_mod.observation_processor.observations) == 15

        assert not game.table[1].active
        assert not game.table[2].active
        assert game.table[3].active
        assert not game.table[4].active
        assert game.table[5].active

        assert game.table[1].chips == 99 #fold
        assert game.table[2].chips == 100 #fold
        assert game.table[3].chips == 95
        assert game.table[4].chips == 99 #fold
        assert game.table[5].chips == 95

    def test_game_added(self):
        self.opp_mod.game_added()
