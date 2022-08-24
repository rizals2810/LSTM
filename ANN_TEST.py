#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 21:29:57 2021

@author: rizal
"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt


class decisions4():
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
        #for idx, item in enumerate(label):
        #    if item < 0.5:
        #        self.target_output.append(0)
        #    else:
        #        self.target_output.append(1)
        
        #self.target_output = np.array(self.target_output).reshape(len(label), 1)
        self.target_output = np.array(label).reshape(len(label), 1)
        return
    
    def train_split(self):
        self.Xtrain, self.Xtest, self.ytrain, self.ytest = train_test_split(self.input_vector, self.target_output, test_size=0.30, random_state=40)
        dtree = DecisionTreeRegressor(max_depth=5, min_samples_leaf=0.13, random_state=3)
        dtree.fit(self.Xtrain, self.ytrain)
        
        pred_train_tree= dtree.predict(self.Xtrain)
        print(np.sqrt(mean_squared_error(self.ytrain,pred_train_tree)))
        print(r2_score(self.ytrain, pred_train_tree))
        
        pred_test_tree= dtree.predict(self.Xtest)
        print(np.sqrt(mean_squared_error(self.ytest,pred_test_tree))) 
        print(r2_score(self.ytest, pred_test_tree))
        print("Hasil prediksi:",pred_test_tree)

        return
    
if __name__ == '__main__':
    p = decisions4()
    p.readfile()
    p.train_split()
    
    