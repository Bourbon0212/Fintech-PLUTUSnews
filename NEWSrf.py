# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:34:51 2020

@author: dx788
"""

import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

with open('word_freq.pkl', 'rb') as file:
    df_t = pickle.load(file)

# 資料預處裡
df_t = df_t.fillna(0)

# Train test data split    
y = df_t['importance'].values
X = df_t.drop(['importance'], axis=1)

# Instantiate rf_cv
rf = RandomForestRegressor()
param_grid = {'n_estimators': list(range(1,30))}
rf_cv = GridSearchCV(rf, param_grid, cv=10)
rf_cv.fit(X, y)
print(rf_cv.best_score_)
print(rf_cv.best_params_)

with open('NEWSrf_model.pkl', 'wb') as file:
    pickle.dump(rf_cv ,file)
    