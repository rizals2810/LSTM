#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:08:55 2021

@author: rizal
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import warnings
warnings.filterwarnings("ignore")


class predictions4():
    def __init__(self, input_vector=[],target_output=[],Xtrain=[],Xtest=[],ytrain=[],ytest=[]):
        self.filename = '/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/SINDSTFLUX_20082013.csv'
        self.input_vector=input_vector
        self.target_output=target_output
        self.Xtrain = Xtrain
        self.Xtest = Xtest
        self.ytrain = ytrain
        self.ytest = ytest
        
    def readfile(self):
        df = pd.read_csv(self.filename)
        feature_cols = ['F10.7', 'DST']
        self.input_vector = df[feature_cols].values
        label = df['S4'].values
        for idx, item in enumerate(label):
            if item < 0.5:
                self.target_output.append(0)
            else:
                self.target_output.append(1)
        
        #self.target_output = np.array(self.target_output).reshape(len(label), 1)
        self.target_output = np.array(self.target_output)
        return
    
    def splitArray(self):
        
        self.Xtrain, self.Xtest, self.ytrain, self.ytest = train_test_split(self.input_vector, self.target_output, test_size=0.20, random_state=42)
        sc = StandardScaler()
        sc.fit(self.Xtrain)
        self.Xtrain = sc.transform(self.Xtrain)
        self.Xtest = sc.transform(self.Xtest)
        
        return
    
    def train(self):
        
        mlp = MLPClassifier(hidden_layer_sizes=(2,2,2), activation='relu', max_iter=100)
        mlp.fit(self.Xtrain, self.ytrain)
        predict = mlp.predict(self.Xtest)
        print(confusion_matrix(self.ytest, predict))
        print(classification_report(self.ytest, predict))
        
        return
    
if __name__ == "__main__":
    p = predictions4()
    p.readfile()
    p.splitArray()
    p.train()
    

    