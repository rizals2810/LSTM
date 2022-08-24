#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 14:58:17 2021

@author: rizal
"""
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


filename = '/Users/rizal/Documents/LAPAN/DSS_NAVIGASI/SINTILASI/FLuxSSNDSTS4_0813.csv'
df = pd.read_csv(filename)
features = np.array(df.drop(columns=['time_tag','S4'],axis=0).values)
dateTime = pd.to_datetime(df['time_tag'])
target = np.array(df['S4'].values)

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.1, random_state=42)

#l_reg = linear_model.LinearRegression()
l_reg = linear_model.Ridge(alpha=0.2, normalize=True, max_iter=500, solver='sag')

model = l_reg.fit(X_train, y_train)

prediction = model.predict(X_test)

print('r2_score:', r2_score(y_test, prediction))
print("Mean square Error:", mean_squared_error(y_test, prediction))

print('Prediction:', prediction[0:10])
print('y_test:', y_test[0:10])
xaxis = [j for j in range(365)]

fig, axs = plt.subplots(2,2)
axs[0, 0].plot(xaxis, features[:365,0])
axs[0, 0].set_title('Flux 10.7')
axs[0, 1].plot(xaxis, features[:365,1])
axs[0, 1].set_title('SSN')
axs[1, 0].plot(xaxis, features[:365,2])
axs[1, 0].set_title('DST')
axs[1, 1].plot(xaxis, target[:365])
axs[1, 1].set_title('S4')

for ax in axs.flat:
    ax.set(xlabel='Count', ylabel='Value')
for ax in axs.flat:
    ax.label_outer()
plt.show()



"""
axs = [j for j in range(len(y_test))]
fig, ax = plt.subplots()
#ax.plot([y_test.min(), y_test.max()],[y_test.min(), y_test.max()],'--r', linewidth=2)
ax.scatter(axs, y_test, alpha=.2)
ax.scatter(axs,prediction, alpha=.2)
#ax.set_xlim([y_test.min(), y_test.max()])
#ax.set_ylim([y_test.min(), y_test.max()])
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')

plt.show()
"""
