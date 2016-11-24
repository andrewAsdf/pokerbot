from pokerbot.game_model import GameState
from pokerbot.game_model import Seat
from pokerbot.controller import Controller


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

    def add_game(self, game):
        pass


class MockOpponentModeller:

    def __init__(self):
        pass

    def game_added(self):
        pass


def create_game_state(table_data, button_seat):
    game_state = GameState()

    for seat_data in table_data:
        seat_number = seat_data['seat_number']

        new_seat = Seat(seat_data['name'], seat_data['stack'])
        new_seat.hand = seat_data['hand']

        game_state.table[seat_number] = new_seat

    game_state.new_game(button_seat)
    return game_state


class TestController:

    def setup_method(self):
        self.game = create_game_state(test_game['table'], test_game['button'])
        self.controller = Controller(self.game, MockDB(), MockOpponentModeller())

    def test_replay(self):
        [self.controller.handle_event(a) for a in test_game['actions']]

        assert self.game.table[1].chips == 99 #fold
        assert self.game.table[2].chips == 100 #fold
        assert self.game.table[3].chips == 95
        assert self.game.table[4].chips == 99 #fold
        assert self.game.table[5].chips == 95

        assert not self.game.table[1].active
        assert not self.game.table[2].active
        assert self.game.table[3].active
        assert not self.game.table[4].active
        assert self.game.table[5].active

