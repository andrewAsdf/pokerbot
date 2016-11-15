from pokerbot.game_model import GameState
from pokerbot.game_model import Seat
from pokerbot.controller import Controller


class _ReplayController(Controller):
    '''Controller class for replaying games'''

    def __init__(self, game):
        super().__init__(game, None, None)

    def game_over(self):
        pass


class OpponentModeller:

    def __init__(self, features, db, teach_interval, observation_processor):
        self.features = features
        self.db = db
        self.observation_processor = observation_processor
        self.teach_interval = teach_interval
        self.unprocessed_game_count = db.unprocessed_game_count
        self.last_processed_game = db.last_processed_game


    def game_added(self):
        self.unprocessed_game_count += 1

        if self.unprocessed_game_count / self.teach_interval >= 1:
            self.process_games()


    def process_games(self):
        games = list(self.db.get_games(self.last_processed_game))

        [self.replay_game(g) for g in games]

        last_id = games[-1]['_id']
        self.last_processed_game = last_id
        self.db.last_processed_game = last_id


    def replay_game(self, game_data):
        game_state = self.create_game_state(game_data['table'], game_data['button'])
        controller = _ReplayController(game_state)

        for action in game_data['actions']:

            if self._is_player_action(action['type']):
                feature_vec = [f(game_state) for f in self.features]
                action_int = self._action_to_int(action['type'])

                self.observation_processor.new_observation(feature_vec, action_int)

            controller.handle_event(action)

        return game_state


    def create_game_state(self, table_data, button_seat):
        game_state = GameState()

        for seat_data in table_data:
            seat_number = seat_data['seat_number']

            new_seat = Seat(seat_data['name'], seat_data['stack'])
            new_seat.hand = seat_data['hand']

            game_state.table[seat_number] = new_seat

        game_state.new_game(button_seat)
        return game_state


    def _is_player_action(self, action_string):
        return action_string in {'fold', 'check', 'call', 'bet', 'raise'}


    def _action_to_int(self, action_string):
        return { 'fold' :  -1,
                 'check':   0,
                 'call' :   0,
                 'bet'  :   1,
                 'raise':   1 }[action_string]
