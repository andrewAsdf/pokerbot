class Seat:

    def __init__ (self, name = '', stack = 0):
        self.name = name
        self.stack = stack
        self.bet  = 0
        self.bet_count = 0
        self.hand = []

    def bet(self, amount):
        self.stack -= amount
        self.bet += amount
        self.bet_count += 1

    def clearBet(self):
        self.bet = 0
        self.bet_count = 0

    def empty(self):
        return True if self.name == '' else False



class Table:

    def __init__ (self):
        self.seats = [Seat() for _ in range(0,10)]
        self.current_seat = 0
        self.button_seat = 0
        self.board = []


    def __getitem__(self, index):
        return self.seats[index]


    def __setitem__(self, key, value):
        self.seats[key] = value


    def nextSeatIndex(self, seatIndex):
        nextIndex = (seatIndex + 1) % 10
        while self.seats[nextIndex].empty:
            nextIndex = (nextIndex + 1) % 10
        return nextIndex


    def clear(self):
        self = Table()


    def moveButton():
        self.button_seat = nextSeatIndex(self.button_seat)


    def nextPlayer():
        self.current_seat = nextSeatIndex(self.current_seat)


class GameState:

    def __init__ (self, big_blind = 1):
        self.stage = 1
        self.table = Table()
        self.big_blind = big_blind
        self.actions = []
        self.out_seat = None


    def perform(self, action):
        if over():
          return
        seat = table.current_seat
        pass

    def reward(self, parent, action):
        pass

    def betAmount(self):
        return self.big_blind if stage < 3 else self.big_blind * 2

    def is_terminal(self):
        pass

    def __eq__(self):
        pass

    def __hash__(self):
        pass

    def postBlinds(self): #todo - 2 players
        sb = table.nextSeatIndex(table.buttonSeat)
        sb.bet(big_blind / 2)
        bb = table.nextSeatIndex(sb)
        bb.bet(big_blind)

