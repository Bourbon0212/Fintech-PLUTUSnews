# -*- coding: utf-8 -*-
"""
Created on Sun May 31 19:32:50 2020

@author: dx788
"""

import pickle
import pandas as pd

from UDNcrawl import UDNcrawl
from CKIPsegmenter import CKIPsegmenter

news = UDNcrawl('防疫概念股', '20200530', '20200530')
news_t = CKIPsegmenter(news, 0)


with open('word_freq.pkl', 'rb') as file:
    df = pickle.load(file)

word_bags = df.columns[0:-1]
     
test = pd.concat([news_t, df])
tt = test.loc[:,word_bags].iloc[0]
