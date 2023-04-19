import requests,os
from bs4 import BeautifulSoup
import threading
from db_client import Mongodb

# 1.爬取北京二手车市场的数据https://www.che168.com/china/a0_0msdgscncgpi1ltocsp5exx0/?pvareaid=102179#currengpostion（5）
# 2.使用requests对网站发起请求把网站的文本信息保存到本地(5分)
# 3.使用beautifulsoup解析网站(2分)
# 4.根据下面的需求爬取相关的数据20页的数据,使用多线程(8分)
# 5.爬取汽车图片到项目指定目录(一般images中) (5分)
# 6.爬取的数据保存到mongodb中(5分)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
}

def save_html():

    url_list=[f'https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{i}exx0/?pvareaid=102179#currengpostion' for i in range(1,21)]
    for i,j in enumerate(url_list):
        res=requests.get(url=j,headers=headers)
        res.encoding=res.apparent_encoding
        with open(f'data/{i+1}.html','w',encoding=res.apparent_encoding)as f:
            f.write(res.text)


def analyse(path='./data/1.html'):
    try:
        soup=BeautifulSoup(open(path,encoding='utf-8'),'lxml')
    except Exception as e:
        soup=BeautifulSoup(open(path,encoding='gbk'),'lxml')
    div_all=soup.find_all(name='div',class_='cards-bottom')
    for i in div_all:
        lt=list(i.stripped_strings)
        try:
            dict1={
                'name':lt[0],
                'logo':lt[0].split(' ')[0],
                'gl':int(lt[1].split('万公里')[0]),
                'sum_price':float(lt[-1].split('万')[0])*10000,
                'm_price':float(lt[-1][:-1])*10000,
            }
        except Exception as e:
            continue
        else:
            Mongodb.table.insert_one(dict1)
            print(dict1)


def save_img(path):
    try:
        soup=BeautifulSoup(open(path,encoding='utf-8'),'lxml')
    except Exception as e:
        soup=BeautifulSoup(open(path,encoding='gbk'),'lxml')
    div_a=soup.find(name='div',id='goodStartSolrQuotePriceCore0')
    try:
        imgs=div_a.find_all(name='img')
    except Exception as e:
        pass
    else:
        for i,j in enumerate(imgs):
            res=requests.get(url='https:'+j['src'],headers=headers)
            with open(f'data/imgs/{i}.png','wb')as f:
                f.write(res.content)

if __name__ == '__main__':
    # save_html()

    urls=os.listdir('./data')
    urls.remove('imgs')

    Mongodb.table.delete_many({})

    for i in urls:
        analyse(path='data/'+i)

    # for i in urls:
    #     save_img('data/'+i)