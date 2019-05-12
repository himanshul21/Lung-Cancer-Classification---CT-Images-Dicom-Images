# -*- coding: utf-8 -*-
"""LUNGCANCER.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sThcGahywuYt7SB1B3C7kyWBrPLumZSW
"""

from google.colab import drive
drive.mount('/content/gdrive')

!pip install pydicom

import my
import return_metadata as rm
import create_batch as cb
import data_augmentation as da

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook

np.random.seed(0)

train_label, index_mal_train, index_beg_train = rm.return_index('train')

train_path, _ = my.return_path('/content/gdrive/My Drive/SPIE-AAPM Lung CT Challenge/Training Set', index_mal_train, index_beg_train)

train_data = my.modified_retrun_data(train_path, 'train')

train_sample = train_data.reshape(10, 100, 100, 100) # num, z, x, y 

Y_train, X_train = cb.modified_create_batchs(train_sample, train_label)

np.random.shuffle(X_train)
np.random.shuffle(Y_train)

test_label, index_mal_test, index_beg_test = rm.return_index('test')

test_path, labels_test = my.return_path('/content/gdrive/My Drive/SPIE-AAPM Lung CT Challenge/Test Set', index_mal_test, index_beg_test)

test_data = my.modified_retrun_data(test_path, 'test')

test_sample = test_data.reshape(-1, 100, 100, 100)

X_test = test_sample.transpose(0, 2, 3, 1)

X_test = X_test.reshape(60, 100, 100, 100, -1)

Y_test = labels_test

import keras
from keras.layers import Dropout, Dense, Conv3D, ZeroPadding3D, Add, Input, AveragePooling3D, MaxPooling3D, Activation, BatchNormalization, Flatten 
from keras.models import Model
from keras.initializers import glorot_uniform

X_train = X_train.transpose(0, 2, 3, 1)
X_train = X_train.reshape(70, 100, 100, 100, -1)
Y_train = keras.utils.to_categorical(Y_train, 2)
Y_test = keras.utils.to_categorical(Y_test, 2)

import model

mod = model.ResNet(input_shape = (100, 100, 100, 1), classes = 2)
mod.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
mod.summary()

mod.fit(X_train, Y_train, epochs = 100, batch_size = 8)

preds = mod.evaluate(X_test, Y_test)

print('Test loss: %0.2f' % (preds[1] * 100))

