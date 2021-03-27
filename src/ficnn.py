import numpy as np
from tensorflow import keras
import tensorflow.keras.backend as K
import tensorflow.keras.layers as L
from .config import Config
from .commons import quantiles as Q


def tilted_loss(q, y, f):
    e = (y - f)
    return K.maximum(q * e, (q - 1) * e)


def make_model(num_layers, q, lr):
    y = keras.Input(shape=(20,))
    last_layer = None
    for i in range(num_layers):
        if last_layer is None:
            last_layer = L.Dense(20, activation='relu')(y)
        else:
            w_z = L.Dense(20)(last_layer)
            w_y = L.Dense(20)(y)
            last_layer = L.add([w_z, w_y])
            last_layer = keras.activations.relu(last_layer)
    out = L.Dense(1)(last_layer)
    model = keras.Model(y, out)
    model.compile(loss=lambda y, f: tilted_loss(q, y, f),
                  optimizer=keras.optimizers.Adam(lr=lr))
    return model


class FICNN:
    def __init__(self, params: Config):
        num_layers = params.values['num_layers']
        lr = params.values['lr']
        self.models = [make_model(num_layers, q, lr) for q in Q]
        self.last_x = None

    def observe(self, y):
        x = self.last_x.reshape(1, 20)
        y = y.reshape(1, 1)
        for model in self.models:
            model.fit(x, y, verbose=0)

    def predict(self, x):
        x = x.reshape(1, 20)
        self.last_x = x
        return np.array([
            np.array(model.predict(x)) for model in self.models
        ]).ravel()


build = FICNN


def get_config():
    return Config({'num_layers': int, 'lr': float})
