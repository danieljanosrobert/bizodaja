import click
import joblib

import neuralnetwork
from constants import EXTENSION_NN, MODEL_NN, DIR_MODEL
from file_manager import dump_file
from jellemzokinyeres import vectorize_tweets, transform_tfidf


def run(model_src, tfidf_src, x_train, y_train, x_test, y_test):
    def init_nn():
        features = click.prompt('features', type=int, default=5000)
        shuffle = click.prompt('shuffle ', type=bool, default=True)
        drop = click.prompt('drop', type=float, default=0.5)
        layer1 = click.prompt('layer1', type=int, default=512)
        layer2 = click.prompt('layer2', type=int, default=256)
        epoch = click.prompt('epoch', type=int, default=5)
        validation = click.prompt('validation', type=float, default=0.1)

        vectorized_tweets = vectorize_tweets(MODEL_NN, x_train, features)

        x_train_mod = transform_tfidf(vectorized_tweets, x_train)
        model_nn = neuralnetwork.train(x_train_mod, y_train, features, shuffle, drop, layer1, layer2, epoch, validation)

        dump_file(model_nn, 'neural network', DIR_MODEL, MODEL_NN, EXTENSION_NN)

        return model_nn, vectorized_tweets

    if model_src and tfidf_src:
        model = joblib.load(model_src)
        tweets = joblib.load(tfidf_src)
    else:
        model, tweets = init_nn()

    x_test_mod = transform_tfidf(tweets, x_test)
    return model.predict_classes(x_test_mod)
