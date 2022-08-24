#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 14:50:36 2021

@author: rizal
"""
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

filename = '/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/SINDSTFLUX_20082013.csv'
df = pd.read_csv(filename)
feature_cols = ['F10.7', 'DST']
input_vector = df[feature_cols].values
target_output = np.array(df['S4'])
Xtrain, Xtest, ytrain, ytest = train_test_split(input_vector, target_output, test_size=0.2, random_state=1)

print("Xtrain:", Xtrain.shape, "Ytrain:", ytrain.shape)
#Mendefinisikan model
model = Sequential()
model.add(Dense(30, input_dim=2, activation='relu'))
model.add(Dense(15, input_dim=2, activation='relu'))
model.add(Dense(1, activation='softmax'))

#Kompile model
#opt = Adam(lr=1e-3, decay=1e-3)
model.compile(loss='mse', optimizer=optimizers.RMSprop(lr=0.01), metrics=['mae'])
h = model.fit(Xtrain, ytrain, validation_data=(Xtest, ytest), epochs=150, batch_size=15)

loss_val = []
for i in h.history['loss']:
    loss_val.append(float("{0:.2f}".format(i)))
val_loss_val = []
for i in h.history['val_loss']:
    val_loss_val.append(float("{0:.2f}".format(i)))
accuracy = []
for i in h.history['mae']:
    accuracy.append(float("{0:.2f}".format(i)))
val_accuracy = [] 
for i in h.history['val_mae']:
    val_accuracy.append(float("{0:.2f}".format(i)))

ypred = model.predict(Xtest)
epochs = range(1, len(loss_val)+1)
plt.figure()
plt.plot(epochs, loss_val, color='red',label='Training loss')
plt.plot(epochs, val_loss_val, color='blue',label='validation loss')
plt.title('Training and Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.figure()
plt.plot(epochs, accuracy, color='green',label='Training accuracy')
plt.plot(epochs, val_accuracy, color='yellow',label='validation accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()
plt.close()


