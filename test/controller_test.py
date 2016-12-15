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


class MockDecisionMaker:

    def get_action(self, game_state):
        return 'call'


class TestController:

    def setup_method(self):
        objects = [MockDB(), MockOpponentModeller(), MockDecisionMaker()]
        self.game = GameState()
        self.controller = Controller(self.game, *objects)

        players = [Seat() for _ in range(10)]
        for p in test_game['table']:
            seat = p['seat_number']
            players[seat] = Seat(p['name'], float(p['stack']))

        self.controller.new_game(players, test_game['button'])

    def test_replay(self):

        self.controller.handle_event(test_game['actions'][0]) #sb
        assert self.game.table[3].chips == 99.5
        self.controller.handle_event(test_game['actions'][1]) #bb
        assert self.game.table[4].chips == 99
        self.controller.handle_event(test_game['actions'][2]) #call 5
        assert self.game.table[5].chips == 99
        self.controller.handle_event(test_game['actions'][3]) #call 1
        assert self.game.table[1].chips == 99
        self.controller.handle_event(test_game['actions'][4]) #fold 2
        assert self.game.table[2].chips == 100
        assert not self.game.table[2].active
        self.controller.handle_event(test_game['actions'][5]) #call 3
        assert self.game.table[3].chips == 99
        self.controller.handle_event(test_game['actions'][6]) #check 4
        assert self.game.table[4].chips == 99
        self.controller.handle_event(test_game['actions'][7]) #flop
        assert self.game.table.board == ["5s", "7c", "Kh"]
        self.controller.handle_event(test_game['actions'][8]) #check 3
        assert self.game.table[3].chips == 99
        self.controller.handle_event(test_game['actions'][9]) #check 4
        assert self.game.table[4].chips == 99
        self.controller.handle_event(test_game['actions'][10]) #check 5
        assert self.game.table[5].chips == 99
        self.controller.handle_event(test_game['actions'][11]) #check 1
        assert self.game.table[1].chips == 99
        self.controller.handle_event(test_game['actions'][12]) #turn
        assert self.game.table.board == ["5s", "7c", "Kh", "Ac"]
        self.controller.handle_event(test_game['actions'][13]) #bet 3
        assert self.game.table[3].chips == 97
        self.controller.handle_event(test_game['actions'][14]) #fold 4
        assert self.game.table[4].chips == 99
        assert not self.game.table[4].active
        self.controller.handle_event(test_game['actions'][15]) #call 5
        assert self.game.table[5].chips == 97
        self.controller.handle_event(test_game['actions'][16]) #fold 1
        assert self.game.table[1].chips == 99
        assert not self.game.table[1].active
        self.controller.handle_event(test_game['actions'][17]) #river
        assert self.game.table.board == ["5s", "7c", "Kh", "Ac", "3s"]
        self.controller.handle_event(test_game['actions'][18]) #bet 3
        assert self.game.table[3].chips == 95
        assert self.game.table[3].active
        self.controller.handle_event(test_game['actions'][19]) #call 5
        assert self.game.table[5].chips == 95
        assert self.game.table[5].active
        self.controller.handle_event(test_game['actions'][20]) #gameover



