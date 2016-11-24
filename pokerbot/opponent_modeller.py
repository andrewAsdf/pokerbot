from pokerbot.game_model import GameState
from pokerbot.game_model import Seat
from pokerbot.controller import Controller

import logging

class _ReplayController(Controller):
    '''Controller class for replaying games'''

    def __init__(self, game):
        super().__init__(game, None, None)

    def game_over(self):
        pass

logger = logging.getLogger('pokerbot.opponent_modeller')


class OpponentModeller:

    def __init__(self, features, db, sample_amount, model_creator, stats):
        self.features = features
        self.db = db
        self.model_creator = model_creator
        self.stats = stats
        self.sample_amount = sample_amount
        self.unprocessed_game_count = db.unprocessed_game_count
        self.last_processed_game = db.last_processed_game
        self.models = {} #for caching models


    def game_added(self):
        self.unprocessed_game_count += 1
        logger.debug('unprocessed: {} games'.format(self.unprocessed_game_count))

        if self.unprocessed_game_count / self.sample_amount >= 1:
            self.process_games()


    def process_games(self):
        '''Calculate all derived data from stored games, including models and
        player statistics'''
        games = list(self.db.get_games())

        self.process_features(games)
        self.process_stats(games)

        self.set_last_processed_game(games[-1])


    def process_features(self, games):
        game_features_list = [self.get_features(g) for g in games]
        game_features = self.feature_list_to_dict(game_features_list)

        for name, features in game_features.items():
            features_transposed = list(zip(*features))
            self.db.add_player_features(name, *features_transposed)

            prev_model = self.db.get_player_model(name) #for incremental learning
            model = self.model_creator.make_model(*features_transposed, prev_model)

            self.db.add_player_model(name, model)
            self.models[name] = model


    def process_stats(self, games):
        stat_dicts = [s(games) for s in self.stats]

        #TODO: merge resulting dicts if there will be more than one stat
        stat_dict = stat_dicts[0]
        
        for player_name, stat in stat_dict.items():
            for stat_name, value in stat_dict[player_name].items():
                self.db.add_player_stat(player_name, stat_name, value)



    def get_features(self, game_data):
        logger.debug('game: {}'.format(game_data['_id']))

        game_state = self.create_game_state(game_data['table'], game_data['button'])
        controller = _ReplayController(game_state)

        game_features = {s.name : [] for s in game_state.table.seats if not s.empty}

        for action in game_data['actions']:
            if self._is_player_action(action['type']):
                feature_vec = [f(game_state) for f in self.features]
                action_int = self._action_to_int(action['type'])
                seat = action['seat']
                game_features[game_state.table[seat].name].append((feature_vec, action_int))
            controller.handle_event(action)
        return game_features


    def create_game_state(self, table_data, button_seat):
        game_state = GameState()

        for seat_data in table_data:
            seat_number = seat_data['seat_number']

            new_seat = Seat(seat_data['name'], seat_data['stack'])
            new_seat.hand = seat_data['hand']

            game_state.table[seat_number] = new_seat

        game_state.new_game(button_seat)
        return game_state


    def set_last_processed_game(self, last_game):
        last_id = last_game['_id']
        self.last_processed_game = last_id
        self.db.last_processed_game = last_id
        self.unprocessed_game_count = 0


    def feature_list_to_dict(self, game_features_list):
        game_features = {}
        for g in game_features_list:
            for name, features in g.items():
                if game_features.get(name) == None:
                    game_features[name] = []
                game_features[name] += features
        return game_features


    def _is_player_action(self, action_string):
        return action_string in {'fold', 'check', 'call', 'bet', 'raise'}


    def _action_to_int(self, action_string):
        return { 'fold' :  -1,
                 'check':   0,
                 'call' :   0,
                 'bet'  :   1,
                 'raise':   1 }[action_string]


    def get_prediction(self, game_state):
        feature_vec = [f(game_state) for f in self.features]
        player_name = game_state.table.current_seat.name

        if (self.models.get(player_name) is None):
            self.models[player_name] = self.db.get_player_model(player_name)

        if (self.models.get(player_name) is not None):
            return self.model_creator.use_model(self.models[player_name], feature_vec)
        else:
            return None
