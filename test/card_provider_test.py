import pokerbot.card_provider
from pokerbot.card_provider import CardProvider

class TestCardProvider:

    def setup_method(self):
        self.card_provider = CardProvider()

    def test_get_board(self):
        flop = self.card_provider.get_flop()
        turn = self.card_provider.get_turn()
        river = self.card_provider.get_river()
        assert not flop[0] in self.card_provider.cards
        assert not flop[1] in self.card_provider.cards
        assert not flop[2] in self.card_provider.cards
        assert not turn in self.card_provider.cards
        assert not river in self.card_provider.cards


    def test_peek_board(self):
        peeked = self.card_provider.peek_board(3)
        assert set(peeked) == set(self.card_provider.get_flop())


    def test_get_hand(self):
        hand = self.card_provider.get_hand()
        assert not hand[0] in self.card_provider.cards
        assert not hand[1] in self.card_provider.cards


    def test_get_hand_vpip(self):
        hand = self.card_provider.get_hand(0.01)
        strength = pokerbot.card_provider.get_hand_strength(*hand)
        assert strength / 169 < 0.01

        hand = self.card_provider.get_hand(0.4)
        strength = pokerbot.card_provider.get_hand_strength(*hand)
        assert strength / 169 < 0.4
        #strength / 169 must be smaller than vpip because 169 is the weakest hand


    def test_remove_card(self):
        self.card_provider.cards = {'Ad', 'Qd', 'Kd'}
        self.card_provider.remove_cards(['Ad', 'Qd'])
        assert len(self.card_provider.cards) == 1


    def test_copy(self):
        card_provider = self.card_provider.copy()
        assert card_provider.peek_board(5) == self.card_provider.peek_board(5)
