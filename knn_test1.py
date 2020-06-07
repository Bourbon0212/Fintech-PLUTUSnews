# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 20:45:10 2020

@author: dx788
"""

import pickle

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

with open('word_freq.pkl', 'rb') as file:
    df_t = pickle.load(file)
    
# 資料預處裡
df_t = df_t.fillna(0)

# Train test data split    
y = df_t['importance'].values
X = df_t.drop(['importance'], axis=1)


# Instantiate knn_cv
knn = KNeighborsClassifier()
param_grid = {'n_neighbors': list(range(1,30))}
knn_cv = GridSearchCV(knn, param_grid, cv=10)
knn_cv.fit(X, y)
print(knn_cv.best_score_)
print(knn_cv.best_params_)