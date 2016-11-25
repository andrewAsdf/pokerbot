from deuces import Card
from deuces import Deck
from deuces import Evaluator
from tabulate import tabulate

from numpy import array
import matplotlib.pyplot as plt

ev = Evaluator()

print("Unknown board:")

hands_num = 200000
values = array([ev.evaluate(Deck().draw(5), []) for i in range(hands_num)])

mean = (7462 - values.mean()) / 7461
std = (values.std()) / 7461

print("Mean: {}, Std: {}".format(mean, std))

count_comb = lambda x, y: sum(x < i <= y for i in values) / hands_num * 100

print(tabulate([["STRAIGHT_FLUSH", "{:10.4f}%".format(count_comb(0, 10))],
["FOUR_OF_A_KIND", "{:10.4f}%".format(count_comb(10, 166))],
["FULL_HOUSE", "{:10.4f}%".format(count_comb(166, 322))],
["FLUSH", "{:10.4f}%".format(count_comb(322, 1599))],
["STRAIGHT", "{:10.4f}%".format(count_comb(1599, 1609))],
["THREE_OF_A_KIND", "{:10.4f}%".format(count_comb(1609, 2467))],
["TWO_PAIR", "{:10.4f}%".format(count_comb(2467, 3325))],
["PAIR", "{:10.4f}%".format(count_comb(3325, 6185))],
["HIGH_CARD", "{:10.4f}%".format(count_comb(6185, 7462))]]))


#bins = [1, 10, 166, 322, 1599, 1609, 2467, 3325, 6185, 7462]
#plt.hist(values, bins)
#plt.show()


