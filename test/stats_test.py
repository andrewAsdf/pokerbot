import pokerbot.stats

test_games = [
{
        "table" : [
                {
                        "hand" : [ ],
                        "name" : "Jagbot",
                        "stack" : 20369.49,
                        "seat_number" : 1
                },
                {
                        "hand" : [ ],
                        "name" : "Jagger",
                        "stack" : 20279.5,
                        "seat_number" : 2
                },
                {
                        "hand" : [ ],
                        "name" : "Lionel",
                        "stack" : 20383.84,
                        "seat_number" : 3
                },
                {
                        "hand" : [ ],
                        "name" : "Malory",
                        "stack" : 20248.75,
                        "seat_number" : 4
                },
                {
                        "hand" : [ ],
                        "name" : "MyBot",
                        "stack" : 18718.42,
                        "seat_number" : 5
                }
        ],
        "button" : 3,
        "actions" : [
                {
                        "amount" : 0.5,
                        "seat" : 4,
                        "type" : "smallBlind"
                },
                {
                        "amount" : 1,
                        "seat" : 5,
                        "type" : "bigBlind"
                },
                {
                        "seat" : 1,
                        "type" : "fold"
                },
                {
                        "seat" : 2,
                        "type" : "fold"
                },
                {
                        "seat" : 3,
                        "type" : "fold"
                },
                {
                        "seat" : 4,
                        "type" : "fold"
                },
                {
                        "wins" : {
                                "5" : 1
                        },
                        "type" : "gameover"
                }
        ]
},
{
        "table" : [
                {
                        "hand" : [ ],
                        "name" : "Jagbot",
                        "stack" : 20369.49,
                        "seat_number" : 1
                },
                {
                        "hand" : [ ],
                        "name" : "Jagger",
                        "stack" : 20279.5,
                        "seat_number" : 2
                },
                {
                        "hand" : [
                                "8c",
                                "8s"
                        ],
                        "name" : "Lionel",
                        "stack" : 20383.84,
                        "seat_number" : 3
                },
                {
                        "hand" : [
                                "Qd",
                                "Kd"
                        ],
                        "name" : "Malory",
                        "stack" : 20248.25,
                        "seat_number" : 4
                },
                {
                        "hand" : [
                                "2c",
                                "9c"
                        ],
                        "name" : "MyBot",
                        "stack" : 18718.92,
                        "seat_number" : 5
                }
        ],
        "button" : 4,
        "actions" : [
                {
                        "amount" : 0.5,
                        "seat" : 5,
                        "type" : "smallBlind"
                },
                {
                        "amount" : 1,
                        "seat" : 1,
                        "type" : "bigBlind"
                },
                {
                        "seat" : 2,
                        "type" : "fold"
                },
                {
                        "amount" : 1,
                        "seat" : 3,
                        "type" : "raise"
                },
                {
                        "seat" : 4,
                        "type" : "call"
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
                        "cards" : [
                                "2d",
                                "Ac",
                                "8d"
                        ],
                        "stage" : "flop",
                        "type" : "board"
                },
                {
                        "seat" : 5,
                        "type" : "check"
                },
                {
                        "amount" : 1,
                        "seat" : 3,
                        "type" : "bet"
                },
                {
                        "seat" : 4,
                        "type" : "call"
                },
                {
                        "seat" : 5,
                        "type" : "call"
                },
                {
                        "cards" : [
                                "2d",
                                "Ac",
                                "8d",
                                "Qs"
                        ],
                        "stage" : "turn",
                        "type" : "board"
                },
                {
                        "seat" : 5,
                        "type" : "check"
                },
                {
                        "amount" : 2,
                        "seat" : 3,
                        "type" : "bet"
                },
                {
                        "seat" : 4,
                        "type" : "call"
                },
                {
                        "seat" : 5,
                        "type" : "call"
                },
                {
                        "cards" : [
                                "2d",
                                "Ac",
                                "8d",
                                "Qs",
                                "4h"
                        ],
                        "stage" : "river",
                        "type" : "board"
                },
                {
                        "seat" : 5,
                        "type" : "check"
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
                        "wins" : {
                                "3" : 16
                        },
                        "type" : "gameover"
                }
        ]
},
{
        "table" : [
                {
                        "hand" : [ ],
                        "name" : "Jagbot",
                        "stack" : 20368.49,
                        "seat_number" : 1
                },
                {
                        "hand" : [
                                "6s",
                                "Ts"
                        ],
                        "name" : "Jagger",
                        "stack" : 20279.5,
                        "seat_number" : 2
                },
                {
                        "hand" : [ ],
                        "name" : "Lionel",
                        "stack" : 20394.84,
                        "seat_number" : 3
                },
                {
                        "hand" : [
                                "3d",
                                "Ad"
                        ],
                        "name" : "Malory",
                        "stack" : 20243.25,
                        "seat_number" : 4
                },
                {
                        "hand" : [
                                "4h",
                                "4s"
                        ],
                        "name" : "MyBot",
                        "stack" : 18713.92,
                        "seat_number" : 5
                }
        ],
        "button" : 5,
        "actions" : [
                {
                        "amount" : 0.5,
                        "seat" : 1,
                        "type" : "smallBlind"
                },
                {
                        "amount" : 1,
                        "seat" : 2,
                        "type" : "bigBlind"
                },
                {
                        "seat" : 3,
                        "type" : "fold"
                },
                {
                        "seat" : 4,
                        "type" : "call"
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
                        "seat" : 2,
                        "type" : "check"
                },
                {
                        "cards" : [
                                "2d",
                                "5h",
                                "Qd"
                        ],
                        "stage" : "flop",
                        "type" : "board"
                },
                {
                        "seat" : 2,
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
                        "cards" : [
                                "2d",
                                "5h",
                                "Qd",
                                "Jh"
                        ],
                        "stage" : "turn",
                        "type" : "board"
                },
                {
                        "seat" : 2,
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
                        "cards" : [
                                "2d",
                                "5h",
                                "Qd",
                                "Jh",
                                "Js"
                        ],
                        "stage" : "river",
                        "type" : "board"
                },
                {
                        "seat" : 2,
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
                        "wins" : {
                                "5" : 3.5
                        },
                        "type" : "gameover"
                }
        ]
}
]


class TestStats:

    def test_vpip_zero(self):
        vpips = pokerbot.stats.vpip([test_games[0]])
        for value in vpips.values():
            assert value['vpip'] == 0

    def test_vpip(self):
        vpips = pokerbot.stats.vpip(test_games)
        assert vpips['Jagbot']['vpip'] == 0
        assert vpips['Jagger']['vpip'] == 0
        assert vpips['Lionel']['vpip'] == 1/3
        assert vpips['Malory']['vpip'] == 2/3
        assert vpips['MyBot']['vpip'] == 2/3
