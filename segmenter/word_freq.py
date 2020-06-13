# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 16:46:55 2020

@author: dx788
"""

import pandas as pd
import pickle

from CKIPsegmenter import CKIPsegmenter

# 生成詞頻矩陣
df = pd.read_csv('UDNcrawler_results.csv', parse_dates = ['time'])
df = df.sort_values("time", ascending=False)
df_t = CKIPsegmenter(df, 6)

# 把 importance 欄位補回來
df_t['importance'] = df['importance'].values

# 暫存詞頻矩陣
with open('word_freq.pkl', 'wb') as file:
   pickle.dump(df_t ,file)