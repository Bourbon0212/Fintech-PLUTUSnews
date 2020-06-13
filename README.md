# PLUTUSnews：防疫概念股新聞分類推播

## 程式碼

### PLUTUSnews.py

    nn, ss = PLUTUSnews('20200529', ['美吾華', '恆大'], 0.8)

* 主程式，相關新聞爬蟲並分類    
* Parameters
   * date (str): Query date
   * stock (list): Interested stock
   * importance (float): Importance sensitivity for news
* Returns
   * news_result (pd.DataFrame): News that regarding the topic
   * stock_result (pd.DataFrame): News that regarding the interested stocks
    
### Module: crawler

#### CYNEScrawl.py

    df = CYNEScrawl('20200402', '20200403')

* Web News Crawler from CYNES.

* Parameters
   * strBegin (str): News start time
   * strEnd (str): News end time

* Returns
   * result (pd.DataFrame): News crawl results

#### UDNcrawl.py

    df = UDNcrawl('防疫', '20200218', '20200219')

* Web News Crawler from UDN.
    
 * Parameters
   * keyword (str): Interested topic
   * strBegin (str): News start time
   * strEnd (str): News end time

 * Returns
   * result (pd.DataFrame): News crawl results

### Module: model

#### NEWSrf.py

* 建立 RandomForest 回歸模型

### Module: segmenter

#### CKIPsegmenter.py

    df_t = CKIPsegmenter(news, 2)

* Generate word terms frequency matrix.
    
* Parameters
   * news (pd.DataFrame): News corpus collect through UDNcrawl
   * threshold (unt): Minimum counts for word terms

* Returns
   * news_t (pd.DataFrame): Word terms frequency matrix from the news
   
 #### word_freq.py
 
 * 生成詞頻矩陣
