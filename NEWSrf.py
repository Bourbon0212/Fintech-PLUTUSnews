# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:34:51 2020

@author: dx788
"""

import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as MSE

with open('word_freq.pkl', 'rb') as file:
    df = pickle.load(file)

# 資料預處裡
df = df.fillna(0)

# Train test data split    
y = df['importance'].values
X = df.drop(['importance'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Instantiate rf
rf = RandomForestRegressor(n_estimators=25,
            random_state=2)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
rmse_test = MSE(y_test, y_pred) ** (1/2)
print('Test set RMSE of rf: {:.2f}'.format(rmse_test))