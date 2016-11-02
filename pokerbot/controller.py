
class Controller:

    def __init__(self, game, db):
        self.game = game
        self.db = db
        self.events = []
        self.seat = 0
        self.cards = tuple()
        pass


    def receive_event(self, event):
        self.events.append(event)
        #TODO: add board cards
        pass


    def new_game(self, players, button_seat):
        self.game.table.seats = players
        self.game.table.button_seat = button_seat
        self.game.new_game()


    def bot_cards(self, cards):
        self.cards = cards


    def bot_seat(self, seat):
        self.seat = seat


    def show_cards(self, seat, cards):
        self.game.table[seat].cards = cards #TODO: card conversion


    def game_over(self):
        seats = [{'name': seat.name, 'seat_number': i, 'hand': seat.hand} for i, seat\
                in enumerate(self.game.table.seats) if not seat.empty]

        last_id = self.db.add_game(seats, self.events, self.game.table.button_seat)

