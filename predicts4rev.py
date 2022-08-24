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
#from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
#from sklearn.metrics import classification_report,confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt


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
        
        label = df['S4']
        """
        for idx, item in enumerate(label):
            if item < 0.5:
                self.target_output.append(0)
            else:
                self.target_output.append(1)
        """
        self.target_output = label
        #self.target_output = np.array(self.target_output).reshape(len(label), 1)
        self.target_output = np.array(self.target_output)
        return
    
    def splitArray(self):
        
        self.Xtrain, self.Xtest, self.ytrain, self.ytest = train_test_split(self.input_vector, self.target_output, test_size=0.20, random_state=1)
        sc = StandardScaler()
        self.Xtrain = sc.fit_transform(self.Xtrain)
        self.Xtest = sc.transform(self.Xtest)
        
        return
    
    def train(self):
        
        #mlp = MLPRegressor(hidden_layer_sizes=(20,20,20), activation='relu',max_iter=2500)
        mlp = make_pipeline(StandardScaler(),
                    MLPRegressor(hidden_layer_sizes=(2,10,7),
                                 tol=1e-2, max_iter=2000, random_state=1, activation='relu'))
        
        h=mlp.fit(self.Xtrain, self.ytrain)
        self.predict = h.predict(self.Xtest)
        self.predict = [float("{0:.2f}".format(i)) for i in self.predict]
        se = []
        for i in range(len(self.ytest)):
            se.append((self.ytest[i]-self.predict[i])**2)
        epochs = range(1, len(self.ytest)+1)
        
        print("Score:", h.score(self.Xtest, self.predict))
        np.set_printoptions(precision=2)
        #print(self.ytest, self.predict)
        
        
        plt.figure()
        plt.title("Actual vs Prediction")
        plt.plot(self.ytest, color='red', label='actual')
        plt.plot(self.predict, color='green', label='prediction')
        plt.xlabel('Epochs')
        plt.ylabel('S4 index')
        plt.legend()
        
        plt.figure()
        plt.title("Error")
        plt.plot(epochs, se, color='red')
        plt.xlabel('Epochs')
        plt.ylabel('error')
        #plt.legend()
        
        plt.show()
        plt.close()
        
        return
    
if __name__ == "__main__":
    p = predictions4()
    p.readfile()
    p.splitArray()
    p.train()
    

    