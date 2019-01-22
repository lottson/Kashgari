# encoding: utf-8
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz

@version: 1.0
@license: Apache Licence
@file: helper.py
@time: 2019-01-19 16:25

"""
import random
from typing import List

import h5py
import numpy as np
from keras.layers import Layer
from keras import backend as K
from keras.preprocessing import sequence
from keras.utils import to_categorical


def h5f_generator(h5path: str,
                  # indices: List[int],
                  num_classes: int,
                  batch_size: int = 128):
    """
    fit generator for h5 file
    :param h5path: target f5file
    :param num_classes: label counts to covert y label to one hot array
    :param batch_size:
    :return:
    """

    db = h5py.File(h5path, "r")
    while True:
        page_list = list(range(len(db['x']) // batch_size + 1))
        random.shuffle(page_list)
        for page in page_list:
            x = db["x"][page: (page + 1) * batch_size]
            y = to_categorical(db["y"][page: (page + 1) * batch_size],
                               num_classes=num_classes,
                               dtype=np.int)
            yield (x, y)


def classification_list_generator(x_data: List,
                                  y_data: List,
                                  sequence_lenght: int,
                                  num_classes: int,
                                  batch_size: int = 128):
    assert len(x_data) == len(y_data)
    while True:
        page_list = list(range(len(x_data) // batch_size + 1))
        random.shuffle(page_list)
        for page in page_list:
            x = x_data[page: (page + 1) * batch_size]
            x = sequence.pad_sequences(x,
                                       maxlen=sequence_lenght)
            y = to_categorical(y_data[page: (page + 1) * batch_size],
                               num_classes=num_classes,
                               dtype=np.int)
            yield (x, y)


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    c = list(zip(a, b))
    random.shuffle(c)
    a, b = zip(*c)
    return list(a), list(b)


class NonMaskingLayer(Layer):
    """
    fix convolutional 1D can't receive masked input, detail: https://github.com/keras-team/keras/issues/4978
    thanks for https://github.com/jacoxu
    """

    def __init__(self, **kwargs):
        self.supports_masking = True
        super(NonMaskingLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        input_shape = input_shape

    def compute_mask(self, input, input_mask=None):
        # do not pass the mask to the next layers
        return None

    def call(self, x, mask=None):
        return x

    def get_output_shape_for(self, input_shape):
        return input_shape


def weighted_categorical_crossentropy(weights):
    """
    A weighted version of keras.objectives.categorical_crossentropy

    Variables:
        weights: numpy array of shape (C,) where C is the number of classes

    Usage:
        weights = np.array([0.5,2,10]) # Class one at 0.5, class 2 twice the normal weights, class 3 10x.
        loss = weighted_categorical_crossentropy(weights)
        model.compile(loss=loss,optimizer='adam')
    """

    weights = K.variable(weights)

    def loss(y_true, y_pred):
        # scale predictions so that the class probas of each sample sum to 1
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
        # clip to prevent NaN's and Inf's
        y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
        # calc
        loss = y_true * K.log(y_pred) * weights
        loss = -K.sum(loss, -1)
        return loss

    return loss


if __name__ == "__main__":
    print("Hello world")