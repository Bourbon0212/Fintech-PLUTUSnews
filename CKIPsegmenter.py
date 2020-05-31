# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:04:25 2020

@author: dx788
"""

import numpy as np
import pandas as pd
import pickle
from ckip import CkipSegmenter
from collections import Counter

def CKIPsegmenter(news, threshold):
    # Initialize CKIP segmenter
    segmenter = CkipSegmenter()
    
    # 將新聞標題與摘要合併
    news['content'] = news['title'] + '\n' + news['summary']

    # 用segmenter斷詞
    news['segment'] = news['content'].apply(lambda x: segmenter.seg(x).tok)

    # Terms of Frequency
    news_t = pd.DataFrame()
    
    for i, row in news.iterrows():
        news_t = news_t.append(pd.DataFrame.from_dict(Counter(row.segment), orient='index').transpose())

    thres = news_t.apply(np.sum, axis=0) > threshold
    news_t = news_t.iloc[:, thres.values]

    return news_t

# df = pd.read_csv('UDN_test.csv')
# df_t = CKIPsegmenter(df, 4)

# 把 importance 欄位補回來
# df_t['importance'] = df['importance'].values

# 暫存詞頻矩陣
# with open('word_freq.pkl', 'wb') as file:
#    pickle.dump(df_t ,file)