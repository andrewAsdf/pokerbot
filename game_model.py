class Seat:

    def __init__ (self, name = '', stack = 0):
        self.name = name
        self.empty = True if name == '' else False
        self.stack = stack
        self.bet  = 0
        self.bet_count = 0

    def bet(amount)
        self.stack -= amount
        self.bet += amount
        self.bet_count += 1


class Table:

    def __init__ (self):
        self.seats = [Seat() for _ in range(0,10)]
        self.current_seat = 0
        self.button_seat = 0


    def __getitem__(self, index):
        return self.seats[index]


    def __setitem__(self, key, value):
        self.seats[key] = value


    def clear(self):
        self = Table()


    def nextSeatIndex(self, seatIndex):
        nextIndex = (seatIndex + 1) % 10
        while self.seats[nextIndex].empty:
            nextIndex = (nextIndex + 1) % 10
        return nextIndex


    def moveButton():
        self.button_seat = nextSeatIndex(self.button_seat)


    def nextPlayer():
        self.current_seat = nextSeatIndex(self.current_seat)


class Game:

    def __init__ (self, table, big_blind = 1):
        self.stage = 1
        self.table = table
        self.big_blind = big_blind

    def postBlinds(self): #todo - 2 players
        sb = table.nextSeatIndex(table.buttonSeat)
        sb.bet(big_blind / 2)
        bb = table.nextSeatIndex(sb)
        bb.bet(big_blind)


    def newGame(self):
        table.moveButton()
        self.postBlinds()


    def nextMove(self):
        if over():
          return
        seat = table.current_seat
        pass

    def over(self):
        pass

    def betAmount(self):
        return self.big_blind if stage < 3 else self.big_blind * 2
