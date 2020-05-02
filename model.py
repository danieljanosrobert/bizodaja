import pandas as pd
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import joblib
from datetime import datetime
from jellemzokinyeres import vectorize_tweets, transform_tfidf
import neuralnetwork


time = datetime.now().strftime("%d%b%Y%H%M%S")


columns = ['label', 'id', 'date', 'flag', 'user', 'text']
sentiment140 = pd.read_csv('./training.1600000.processed.noemoticon.csv', header=None, names=columns, encoding='latin1')

#Neural Network
def model1(X_train, y_train):
    features = 5000
    shuffle = True
    drop = 0.5
    layer1 = 512
    layer2 = 256
    epoch = 5
    validation = 0.1
    vectorized_tweets = vectorize_tweets(X_train, features)
    X_train_mod = transform_tfidf(vectorized_tweets)
    model = neuralnetwork.train(X_train_mod, y_train, features, shuffle, drop, layer1, layer2, epoch, validation)
    joblib.dump(model, 'model_' + time + '.file')
    return model


sentiment140['label'] = sentiment140['label'].apply(lambda x: 1 if x == 4 else 0)
X_train, X_test, y_train, y_test = train_test_split(sentiment140['text'], sentiment140['label'], test_size=0.2, shuffle=True)

data_quantity = 10000 # mennyi adaton tanítsunk

X_train = X_train.head(data_quantity).values
y_train = y_train.head(data_quantity).values
X_test = X_test.head(round(data_quantity*0.2)).values
y_test = y_test.head(round(data_quantity*0.2)).values

y_train = to_categorical(y_train)

# model, vocabulary = model1(X_train, y_train)

model = joblib.load('./model_01May2020221931.file')
tweets = joblib.load('./fitted_tfidf_01May2020221931.file')

X_test_mod = tweets.transform(X_test).toarray()
y_test = to_categorical(y_test)

result = model.evaluate(X_test_mod, y_test)

print('---')
print(model.metrics_names)
print(result)
