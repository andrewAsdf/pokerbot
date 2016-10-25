class GameSynchronizer:

    def __init__(self, gameState):
        self.gameState = gameState

    def bet(self, event):
        pass

    def bigBlind(self, event):
        pass

    def board(self, event):
        pass

    def call(self, event):
        pass

    def check(self, event):
        pass

    def fold(self, event):
        pass

    def muck(self, event):
        pass

    def smallBlind(self, event):
        pass

    def sync(event):
        getattr(self, [event['type']]())(event)
