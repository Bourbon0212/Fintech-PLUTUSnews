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
    
    '''
    Generate word terms frequency matrix.
    
    Parameters:
        news (pd.DataFrame): News corpus collect through UDNcrawl
        threshold (unt): Minimum counts for word terms

    Returns:
        news_t (pd.DataFrame): Word terms frequency matrix from the news
    '''   
    
    # 讀入停用詞
    with open('segmenter\stopWords.pkl', 'rb') as file:
        stopWords = pickle.load(file)
    
    # Initialize CKIP segmenter
    segmenter = CkipSegmenter()
    
    # 將新聞標題與摘要合併
    news['content'] = news['title'] + '\n' + news['summary']

    # 用segmenter斷詞
    # news['content'] = news['content'].apply(lambda x: x.encode('cp950')) # 解決cp950問題，但還不work
    news['segment'] = news['content'].apply(lambda x: segmenter.seg(x).tok)
    news['segment'] = news['segment'].apply(lambda x: list(filter(lambda a: a not in stopWords and a != '\n', x)))

    # Terms of Frequency
    news_t = pd.DataFrame()
    
    for i, row in news.iterrows():
        news_t = news_t.append(pd.DataFrame.from_dict(Counter(row.segment), orient='index').transpose())

    thres = news_t.apply(np.sum, axis=0) > threshold
    news_t = news_t.iloc[:, thres.values]

    return news_t
