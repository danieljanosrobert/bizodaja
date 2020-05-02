import click
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

from constants import MODEL_SGD, EXTENSION_SGD, OPTION_SGD, OPTION_LOGR, MODEL_LOGR, EXTENSION_LOGR, DIR_MODEL
from file_manager import dump_file
from jellemzokinyeres import vectorize_tweets, transform_tfidf


def run(selected_model, model_src, tfidf_src, x_train, y_train, x_test, y_test):

    def init_model(classifier_model, model_name, model_extension):
        features = click.prompt('features', type=int, default=5000)
        vectorized_tweets = vectorize_tweets(model_name, x_train, features)
        x_train_mod = transform_tfidf(vectorized_tweets, x_train)
        classifier_model = classifier_model
        classifier_model.fit(x_train_mod, y_train)

        dump_file(classifier_model, 'classifier model', DIR_MODEL, model_name, model_extension)

        return classifier_model, vectorized_tweets

    if model_src and tfidf_src:
        model = joblib.load(model_src)
        tweets = joblib.load(tfidf_src)
    elif selected_model == OPTION_SGD:
        model, tweets = init_model(SGDClassifier(), MODEL_SGD, EXTENSION_SGD)
    elif selected_model == OPTION_LOGR:
        model, tweets = init_model(LogisticRegression(), MODEL_LOGR, EXTENSION_LOGR)
    else:
        raise RuntimeError('No operation for selected model!')

    x_test_mod = transform_tfidf(tweets, x_test)
    return model.predict(x_test_mod)
