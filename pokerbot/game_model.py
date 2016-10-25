import enum

class Action(enum.Enum):
    Fold = 1
    Call = 2
    Raise = 3


class Seat:

    def __init__ (self, name = '', chips = 0):
        self.name = name
        self.chips = chips
        self.chips_bet  = 0
        self.bet_count = 0
        self.hand = []
        self.active = False

    def bet(self, amount):
        self.chips -= amount
        self.chips_bet += amount
        self.bet_count += 1

    def reset(self):
        self.chips_bet = 0
        self.bet_count = 0
        self.active = True if self.chips > 0 else False

    def fold(self):
        self.active = False

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


    def nextSeatIndex(self, seatIndex, neighbor = 1):

        nextIndex = seatIndex

        while neighbor > 0:
            nextIndex = (nextIndex + 1) % 10
            if not self.seats[nextIndex].empty():
                neighbor -= 1

        return nextIndex


    def clear(self):
        self = Table()


    def newGame(self):
        map(lambda x: x.reset(), seats)
        moveButton()
        

    def moveButton(self):
        self.button_seat = self.nextSeatIndex(self.button_seat)


    def nextPlayer(self):
        self.current_seat = self.nextSeatIndex(self.current_seat)


    def getSmallBlindSeat(self):
        return nextSeatIndex(self.button_seat, 1)

    def getBigBlindSeat(self):
        return nextSeatIndex(self.button_seat, 2)

    def getFirstPlayerSeat(self):
        return nextSeatIndex(self.button_seat, 3)



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
