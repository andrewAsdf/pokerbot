from pymongo import MongoClient


class Database:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.poker
        self.games = self.db.games

    def add_game(self, seats, actions, button_seat):
        game = {}
        game['actions'] = actions
        game['table'] = seats
        game['button'] = button_seat

        for seat in seats:
            pass

        object_id = self.games.insert_one(game).inserted_id
        return object_id
