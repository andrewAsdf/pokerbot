from pymongo import MongoClient
from bson.objectid import ObjectId
import pickle


NULL_ID = ObjectId("000000000000000000000000")


class Database:
    def __init__(self, mongo_port = 27017):
        self.client = MongoClient('localhost', mongo_port)
        self.db = self.client.poker
        self.games = self.db.games
        self.meta = self.db.meta
        self.models = self.db.models
        self.features = self.db.features
        self.opponentmodels = self.db.opponentmodels

        self.meta.update({ '_id': 1 },
                         { '$setOnInsert': {'lastProcessedGame': NULL_ID}, },
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


    def get_games(self):
        return self.games.find({'_id': {'$gt' : self.last_processed_game}})


    @property
    def unprocessed_game_count(self):
        return self.games.count({'_id': {'$gt' : self.last_processed_game}})


    def add_player_model(self, player_name, model):
        model_data = pickle.dumps(model)
        update = {
                    '$set' : {'model' : pickle.dumps(model)},
                    '$setOnInsert' : {'name' : player_name}
                 }
        self.models.update({'name': player_name}, update, upsert = True)


    def get_player_model(self, player_name):
        found = self.models.find_one({'name' : player_name})
        if found is not None:
            return pickle.loads(found['model'])
        else:
            return None


    def add_player_features(self, player_name, inputs, responses):
        update = {
                    '$set' : {'inputs' : inputs, 'responses':responses},
                    '$setOnInsert' : {'name' : player_name}
                 }
        self.features.update({'name': player_name}, update, upsert = True)


    def get_player_features(self, player_name):
        return self.features.find_one({'name': player_name})
