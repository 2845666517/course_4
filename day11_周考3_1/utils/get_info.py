import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from sqlalchemy import create_engine
from databases import engine

def save_html():
    print('正在保存')
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }
    res=requests.get(url=url,headers=headers)
    res.encoding='utf-8'
    with open('res.html','w',encoding='utf-8')as f:
        f.write(res.text)
    print('保存完成')

def save_sql():
    df=pd.read_html('./res.html')[0]
    df.columns = ['rank','school','address','sum_score','score']
    df['id']=df.index+1
    df.to_sql('college',con=engine,index=False,if_exists='replace')
    print('保存完成')

if __name__ == '__main__':
    url='https://www.phb123.com/jiaoyu/gx/31470.html'
    # if os.path.exists('./res.html') is False:
    #     save_html()
    save_sql()