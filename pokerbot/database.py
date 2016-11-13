from pymongo import MongoClient
from bson.objectid import ObjectId


nullId = ObjectId("000000000000000000000000")


class Database:
    def __init__(self, mongo_port = 27017):
        self.client = MongoClient('localhost', mongo_port)
        self.db = self.client.poker
        self.games = self.db.games
        self.meta = self.db.meta
        self.opponentmodels = self.db.opponentmodels

        self.meta.update({ '_id': 1 },
                         { '$setOnInsert': {'lastProcessedGame': nullId}, },
                         upsert = True)

    def add_game(self, seats, actions, button_seat):
        game = {}
        game['actions'] = actions
        game['table'] = seats
        game['button'] = button_seat

        for seat in seats:
            pass

        object_id = self.games.insert_one(game).inserted_id
        return object_id


    @property
    def last_processed_game(self):
        return self.meta.find_one({'_id': 1})['lastProcessedGame']


    @last_processed_game.setter
    def last_processed_game(self, game_id):
        self.meta.update({'_id':1}, {"$set": {'lastProcessedGame' : game_id}})


    def get_games(self, from_id = nullId):
        return self.games.find({'_id': {'$gt' : from_id}})


    @property
    def unprocessed_game_count(self):
        return self.games.count({'_id': {'$gt' : self.last_processed_game}})


