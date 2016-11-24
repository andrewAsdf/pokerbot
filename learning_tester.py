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

X = features[players[0]]['inputs']
y = features[players[0]]['responses']

X_train = np.matrix(X)
y_train = np.array(y)

X_test = np.matrix(X)
y_test = np.array(y)

model = MLPClassifier(hidden_layer_sizes = [7, 5], max_iter = 2000)

fold_number = 20

print("Training with {}-fold crossvalidation".format(fold_number))
results = cross_val_score(model, X[:2000], y[:2000], cv = fold_number)

print("Average training accuracy: {}".format(results.mean()))

test_score = model.fit(X_train, y_train).score(X_test, y_test)
print("Testing accuracy: {}".format(test_score))

