import click
import pandas as pd
from keras.utils import to_categorical
from evaluation import evaluate
from sklearn.model_selection import train_test_split

import model_classifier_facotry
import model_neuralnet
from constants import OPTION_NN, OPTION_LOGR, OPTION_SGD, DIR_REPORT, EXTENSION_REPORT
from file_manager import dump_file


def init_model(database_src, model, model_src, tfidf_src):

    print('Please wait, the database is being prepared for use\n')
    columns = ['label', 'id', 'date', 'flag', 'user', 'text']
    data = pd.read_csv(database_src, header=None, names=columns, encoding='latin1')

    data['label'] = data['label'].apply(lambda x: 1 if x == 4 else 0)
    x_train, x_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, shuffle=True)

    print('Please set up your model!')
    if not model_src:
        data_quantity = click.prompt('Train data quantity', type=int, default=10000)  # mennyi adaton tanítsunk
        data_quantity = len(y_train) if data_quantity > len(y_train) else data_quantity
        x_train = x_train.head(data_quantity).values
        y_train = y_train.head(data_quantity).values

    test_quantity = click.prompt('Test data quantity', type=int, default=2000)  # mennyi adaton teszteljünk
    test_quantity = len(y_test) if test_quantity > len(y_test) else test_quantity
    x_test = x_test.head(test_quantity).values
    y_test = y_test.head(test_quantity).values

    if model == OPTION_NN:
        y_train = to_categorical(y_train)
        y_pred = model_neuralnet.run(model_src, tfidf_src, x_train, y_train, x_test, y_test)
    elif model in (OPTION_LOGR, OPTION_SGD):
        y_pred = model_classifier_facotry.run(model, model_src, tfidf_src, x_train, y_train, x_test, y_test)
    else:
        raise RuntimeError('No operation for selected model!')

    evaluate(y_test, y_pred)
    dump_file((y_test, y_pred), 'report', DIR_REPORT, 'report', EXTENSION_REPORT)
