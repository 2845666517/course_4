import os
import requests
from bs4 import BeautifulSoup
from db_client import Pymongo

def save_html(res):
    res.encoding='utf-8'
    with open('res.html','w',encoding='utf-8')as f:
        f.write(res.text)


def get_author(soup):
    div_a=soup.find(name='div',class_='sjk_con')
    ul_a=div_a.find(name='ul')
    li_all=ul_a.find_all(name='li')
    a_list=[]

    # 4.
    # 获取所有的作家的子页面链接
    Pymongo.table.delete_many({})
    for i in li_all:
        dict1={'name':i.find(name='a')['title'],'链接':'http://literature.cssn.cn/ldzjsjk/'+i.find(name='a')['href'][1:]}
        a_list.append(dict1)
    Pymongo.table.insert_many(a_list)

def save_text():
    all_href=Pymongo.table.find()
    for j,i in enumerate(all_href):
        res=requests.get(url=i['链接'],headers=headers)
        res.encoding='utf-8'
        with open(f'data/page{j+1}.html','w',encoding='utf-8')as f:
            f.write(res.text)


def save_author_xiangxi():
    file_list=os.listdir('./data')
    for i in file_list:
        soup=BeautifulSoup(open(f'data/{i}',encoding='utf-8'),'lxml')
        div_a=soup.find(name='div',class_='top')
        p_all=div_a.find_all(name='p')
        lt2=['战国','五代','汉末']
        dict1={}
        for i in p_all:
            text=list(i.stripped_strings)
            if len(text)==1:
                text.append('无')
            dict1[text[0]]=text[1]

        if dict1['朝代：'] in lt2:
            cs='公元前'
        else:
            cs='公元后'
        dict1['出生']=cs
        Pymongo.table2.insert_one(dict1)




if __name__ == '__main__':
    url='http://literature.cssn.cn/ldzjsjk/'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }
    # res=requests.get(url=url,headers=headers)
    # save_html(res)

    # 3.爬取历代作家研究数据库网站：http://literature.cssn.cn/ldzjsjk/
    # Pymongo.table.delete_many({})
    # soup=BeautifulSoup(open('res.html',encoding='utf-8'),'lxml')
    # get_author(soup)

    # 保存所有作者网页
    # save_text()

    # 信息保存到数据库
    # Pymongo.table2.delete_many({})
    # save_author_xiangxi()
    # print(list(Pymongo.table2.find()))




