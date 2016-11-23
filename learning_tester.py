from pymongo import MongoClient
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
import pokerbot.database

db = pokerbot.database.Database()
players = ['Jagbot', 'Malory', 'Lionel', 'Jagger']

features = {n : db.get_player_features(n) for n in players}
tp_number = len(features[players[0]])

print('Training points: {}'.format(tp_number))

X_train = np.matrix(features[players[0]]['inputs'][100:])
y_train = np.array(features[players[0]]['responses'][100:])

X_test = np.matrix(features[players[0]]['inputs'][:100])
y_test = np.array(features[players[0]]['responses'][:100])

model = MLPClassifier(hidden_layer_sizes = [7, 5], max_iter = 300)

fold_number = 6

print("Training with {}-fold crossvalidation".format(fold_number))
results = cross_val_score(model, X_test, y_test, cv = fold_number)

print("Average training accuracy: {}".format(results.mean()))


