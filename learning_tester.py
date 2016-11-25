from pymongo import MongoClient
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from operator import iadd
import numpy as np
import numpy.matlib as matlib
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


#layer_sizes = [[5, 5], [7, 5], [15, 12], [20, 17], [15, 12, 10], [30, 25]]
#results = [train_with_layers(s) for s in layer_sizes]
#print(tabulate(zip(layer_sizes, results), headers=['Layer sizes', 'Score']))


def get_confusion_matrix(results):
    answer_comp = list(zip(y_test, results))

    conf = matlib.zeros((3, 3))
    for comp in answer_comp:
        conf[comp[0] + 1,comp[1] + 1] += 1

    conf = conf / len(answer_comp)

    return [
            ['Fold', conf[0,0], conf[0,1], conf[0,2]],
            ['Call', conf[1,0], conf[1,1], conf[1,2]],
            ['Raise', conf[2,0], conf[2,1], conf[2,2]],
    ]


model = MLPClassifier(hidden_layer_sizes = [20, 17], max_iter = 2000)
results = model.fit(X_train, y_train).predict(X_test)

headers = ['Act\Pred', 'Fold', 'Call', 'Raise']
print(tabulate(get_confusion_matrix(results), headers=headers, floatfmt='.2f'))


