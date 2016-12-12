from random import Random

class ckCardProvider:

    def __init__(self, seed = 420, no_shuffle = False):
        self.random = Random(seed)
        self.no_shuffle = no_shuffle
        self.reset()


    def get_hand(self, vpip = 1):
        return [self.cards.pop(), self.cards.pop()]


    def get_flop(self):
        return [self.cards.pop(), self.cards.pop(), self.cards.pop()]


    def get_turn(self):
        return self.cards.pop()


    def get_river(self):
        return self.cards.pop()


    def peek_cards(self, number):
        return self.cards[-number:]


    def shuffle(self):
        if not self.no_shuffle:
            self.random.shuffle(self.cards)


    def reset(self):
        self.cards = [ '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td',
            'Jd', 'Qd', 'Kd', 'Ad', '2c', '3c', '4c', '5c', '6c', '7c', '8c',
            '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac', '2s', '3s', '4s', '5s', '6s',
            '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As', '2h', '3h', '4h',
            '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah' ]


    def remove_cards(self, removed_cards):
        [self.cards.remove(c) for c in removed_cards]


    def copy(self):
        new_prov = copy(self)
        new_prov.cards = copy(self.cards)
        return new_prov


_hand_values = {'AA' : 1, 'KK' : 2, 'QQ' : 3, 'AKs' : 4,
'JJ' : 5, 'AQs' : 6, 'KQs' : 7, 'AJs' : 8,
'KJs' : 9, 'TT' : 10, 'AKo' : 11, 'ATs' : 12,
'QJs' : 13, 'KTs' : 14, 'QTs' : 15, 'JTs' : 16,
'99' : 17, 'AQo' : 18, 'A9s' : 19, 'KQo' : 20,
'88' : 21, 'K9s' : 22, 'T9s' : 23, 'A8s' : 24,
'Q9s' : 25, 'J9s' : 26, 'AJo' : 27, 'A5s' : 28,
'77' : 29, 'A7s' : 30, 'KJo' : 31, 'A4s' : 32,
'A3s' : 33, 'A6s' : 34, 'QJo' : 35, '66' : 36,
'K8s' : 37, 'T8s' : 38, 'A2s' : 39, '98s' : 40,
'J8s' : 41, 'ATo' : 42, 'Q8s' : 43, 'K7s' : 44,
'KTo' : 45, '55' : 46, 'JTo' : 47, '87s' : 48,
'QTo' : 49, '44' : 50, '22' : 51, '33' : 52,
'K6s' : 53, '97s' : 54, 'K5s' : 55, '76s' : 56,
'T7s' : 57, 'K4s' : 58, 'K2s' : 59, 'K3s' : 60,
'Q7s' : 61, '86s' : 62, '65s' : 63, 'J7s' : 64,
'54s' : 65, 'Q6s' : 66, '75s' : 67, '96s' : 68,
'Q5s' : 69, '64s' : 70, 'Q4s' : 71, 'Q3s' : 72,
'T9o' : 73, 'T6s' : 74, 'Q2s' : 75, 'A9o' : 76,
'53s' : 77, '85s' : 78, 'J6s' : 79, 'J9o' : 80,
'K9o' : 81, 'J5s' : 82, 'Q9o' : 83, '43s' : 84,
'74s' : 85, 'J4s' : 86, 'J3s' : 87, '95s' : 88,
'J2s' : 89, '63s' : 90, 'A8o' : 91, '52s' : 92,
'T5s' : 93, '84s' : 94, 'T4s' : 95, 'T3s' : 96,
'42s' : 97, 'T2s' : 98, '98o' : 99, 'T8o' : 100,
'A5o' : 101, 'A7o' : 102, '73s' : 103, 'A4o' : 104,
'32s' : 105, '94s' : 106, '93s' : 107, 'J8o' : 108,
'A3o' : 109, '62s' : 110, '92s' : 111, 'K8o' : 112,
'A6o' : 113, '87o' : 114, 'Q8o' : 115, '83s' : 116,
'A2o' : 117, '82s' : 118, '97o' : 119, '72s' : 120,
'76o' : 121, 'K7o' : 122, '65o' : 123, 'T7o' : 124,
'K6o' : 125, '86o' : 126, '54o' : 127, 'K5o' : 128,
'J7o' : 129, '75o' : 130, 'Q7o' : 131, 'K4o' : 132,
'K3o' : 133, '96o' : 134, 'K2o' : 135, '64o' : 136,
'Q6o' : 137, '53o' : 138, '85o' : 139, 'T6o' : 140,
'Q5o' : 141, '43o' : 142, 'Q4o' : 143, 'Q3o' : 144,
'74o' : 145, 'Q2o' : 146, 'J6o' : 147, '63o' : 148,
'J5o' : 149, '95o' : 150, '52o' : 151, 'J4o' : 152,
'J3o' : 153, '42o' : 154, 'J2o' : 155, '84o' : 156,
'T5o' : 157, 'T4o' : 158, '32o' : 159, 'T3o' : 160,
'73o' : 161, 'T2o' : 162, '62o' : 163, '94o' : 164,
'93o' : 165, '92o' : 166, '83o' : 167, '82o' : 168,
'72o' : 169}

_hand_ranks = {
        '2' : '2',
        '3' : '3',
        '4' : '4',
        '5' : '5',
        '6' : '6',
        '7' : '7',
        '8' : '8',
        '9' : '9',
        'T' : 'A',
        'J' : 'B',
        'K' : 'C',
        'A' : 'D',
        }
#hand rank ordering is done lexicographically

def get_hand_value(card1, card2):
    """
    Return the starting hand value ranging from 1 to 169, where the weakest
    hand is 169. Arguments must be in the standard string format.
    """
    rank1 = card1[0]
    suit1 = card1[1]
    rank2 = card2[0]
    suit2 = card2[1]

    suited = 's' if suit1 == suit2 else 'o'

    if _hand_ranks[rank2] < _hand_ranks[rank1]:
        return (_hand_values[rank1 + rank2 + suited])

    elif _hand_ranks[rank2] > _hand_ranks[rank1]:
        return (_hand_values[rank2 + rank1 + suited])

    else:
        return (_hand_values[rank2 + rank1])
