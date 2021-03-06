from copy import deepcopy


stage_numbers = {'flop' : 1, 'turn' : 2, 'river' : 3}


class Controller:

    def __init__(self, game, db, opponent_modeller, decision_maker):
        self.game = game
        self.db = db
        self.events = []
        self.seat = 0
        self.seats_initial = [] #for storing in db
        self.cards = tuple()
        self.playing = False
        self.opponent_modeller = opponent_modeller
        self.decision_maker = decision_maker


    def receive_event(self, event):
        if not self.playing:
            return
        self.events.append(event)
        self.handle_event(event)


    def get_action(self):
        if not self.playing:
            return 0
        return self.decision_maker.get_action(self.game, max_iter=1000)


    def handle_event(self, event):
        if not self.playing:
            return
        type = event['type']

        if type == 'board':
            self.game.table.board = event['cards']
            self.game.next_stage()
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


    def new_game(self, players, button_index):
        self.playing = True
        self.events = []

        self.game.table.seats = players
        self.seats_initial = deepcopy(players) #for storing in db

        self.game.new_game(button_index)


    def bot_cards(self, cards):
        if not self.playing:
            return
        self.cards = cards
        self.game.table[self.seat].hand = cards


    def bot_seat(self, seat):
        if not self.playing:
            return
        self.seat = seat


    def show_cards(self, seat, cards):
        if not self.playing:
            return

        self.game.table[seat].hand = cards
        self.seats_initial[seat].hand = cards


    def game_over(self):
        self.playing = False
        game_data = self.create_game_data()
        self.db.add_game(game_data)

        self.opponent_modeller.game_added()


    def create_game_data(self):
        seats = [{
                    'name': seat.name,
                    'seat_number': i,
                    'hand': seat.hand,
                    'stack': seat.chips
                 }
                 for i, seat in enumerate(self.seats_initial) if not seat.empty]

        return {
            'actions' : self.events,
            'table' : seats,
            'button' : self.game.table.button_index
        }


