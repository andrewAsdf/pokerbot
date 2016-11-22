from sklearn.neural_network import MLPClassifier


def make_model(inputs, answers, prev_model = None):
    if prev_model is None:
        model = MLPClassifier(hidden_layer_sizes = [7, 5])
        model.fit(inputs, answers)
        return model
    else:
        prev_model.partial_fit(inputs, answers)
        return prev_model


def use_model(model, feature_vec):
    return model.predict(feature_vec)


