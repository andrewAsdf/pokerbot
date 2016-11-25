from pymongo import MongoClient
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
import pokerbot.database
from tabulate import tabulate

db = pokerbot.database.Database()
players = ['Jagbot', 'Malory', 'Lionel', 'Jagger']

features = {n : db.get_player_features(n) for n in players}

X = features[players[0]]['inputs']
y = features[players[0]]['responses']

X_train = np.matrix(X)
y_train = np.array(y)

X_test = np.matrix(X)
y_test = np.array(y)

#fold_number = 20
#print("Training with {}-fold crossvalidation".format(fold_number))
#results = cross_val_score(model, X[:2000], y[:2000], cv = fold_number)
#print("Average training accuracy: {}".format(results.mean()))

def train_with_layers(layer_sizes):
    model = MLPClassifier(hidden_layer_sizes = layer_sizes, max_iter = 2000)
    print('Training with {}'.format(layer_sizes))
    return model.fit(X_train, y_train).score(X_test, y_test)

layer_sizes = [[5, 5], [7, 5], [15, 12], [20, 17], [15, 12, 10], [30, 25]]

results = [train_with_layers(s) for s in layer_sizes]

print(tabulate(zip(layer_sizes, results), headers=['Layer sizes', 'Score']))
