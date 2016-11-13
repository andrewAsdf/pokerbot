from pokerbot.game_model import GameState
from pokerbot.game_model import Seat

class OpponentModeller:

    def __init__(self, features, db, teach_interval):
        sele.features = features
        self.db = db
        self.teach_interval = teach_interval
        self.unprocessed_game_count = db.unprocessed_game_count
        self.last_processed_game = db.last_processed_game


    def game_added(self):
        self.unprocessed_game_count += 1

        if self.unprocessed_game_count / teach_interval >= 1:
            self.process_games()


    def process_games(self):
        games = list(db.get_games(self.last_processed_game))

        for game in games:
            game_state = create_game_state(game['table'], game['button'])

        last_id = games[-1]['_id']
        self.last_processed_game = last_id
        db.last_processed_game = last_id


    def create_game_state(self, table_data, button_seat):
        game_state = GameState()

        for seat_data in table_data['table']:
            seat_number = seat_data['seat_number']

            new_seat = Seat(seat_data['name'], seat_data['stack'])
            new_seat.hand = seat_data['hand']

            game_state.table[seat_number] = new_seat

        game_state.new_round(button_seat)


