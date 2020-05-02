import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout

def train(X_train_mod, y_train, features, shuffle, drop, layer1, layer2, epoch, validation):
    model_nn = Sequential()
    model_nn.add(Dense(layer1, input_shape=(features,), activation='relu'))
    model_nn.add(Dropout(drop))
    model_nn.add(Dense(layer2, activation='sigmoid'))
    model_nn.add(Dropout(drop))
    model_nn.add(Dense(2, activation='softmax'))

    model_nn.compile(loss='binary_crossentropy',
                     optimizer='adam',
                     metrics=['accuracy'])

    model_nn.fit(np.array(X_train_mod), y_train,
                 batch_size=32,
                 epochs=epoch,
                 verbose=1,
                 validation_split=validation,
                 shuffle=shuffle)
    return model_nn