from copy import deepcopy


stage_numbers = {'flop' : 1, 'turn' : 2, 'river' : 3}


class Controller:

    def __init__(self, game, db, opponentmodeller):
        self.game = game
        self.db = db
        self.events = []
        self.seat = 0
        self.cards = tuple()
        self.playing = False
        self.opponentmodeller = opponentmodeller


    def receive_event(self, event):
        if not self.playing:
            return
        self.events.append(event)
        self.handle_event(event)


    def handle_event(self, event):
        type = event['type']

        if type == 'board':
            self.game.table.board = event['cards']
            self.game._next_stage() #todo - game should know this
        elif type == 'bet' or type == 'raise':
            self.game.bet()
        elif type == 'call' or type == 'check':
            self.game.call()
        elif type == 'fold':
            self.game.fold()
        elif type == 'gameover':
            self.game_over()
        elif type == 'bigBlind' or type == 'smallBlind':
            pass
        else:
            raise RuntimeError('Invalid event type: {}'.format(type))


    def new_game(self, players, button_seat):
        self.playing = True
        self.events = []
        self.game.table.seats = players
        self.game.table.button_seat = button_seat

        self.seats_initial = deepcopy(players) #for storing in db

        self.game.new_game()


    def bot_cards(self, cards):
        self.cards = cards


    def bot_seat(self, seat):
        self.seat = seat


    def show_cards(self, seat, cards):
        if not self.playing:
            return

        self.game.table[seat].hand = cards
        self.seats_initial[seat].hand = cards


    def game_over(self):
        self.playing = False
        seats = [{
                    'name': seat.name,
                    'seat_number': i,
                    'hand': seat.hand,
                    'stack': seat.chips
                 }
                 for i, seat in enumerate(self.seats_initial) if not seat.empty]

        self.db.add_game(seats, self.events, self.game.table.button_seat)

        self.opponentmodeller.game_added()

        self.game.new_game()

