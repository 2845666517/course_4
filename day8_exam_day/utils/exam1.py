# 1．导入相关三方库
import json
import re
import time,pymongo
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from client_db import Mongodb


client = pymongo.MongoClient(
    host='127.0.0.1',
    port=27017
)
db = client['2010_rk08']
table = db['2010_ro08']


def run(p,url):
    # 1找到浏览器
    chrom=p.chromium.launch(headless=False)
    # 2打开浏览器
    page=chrom.new_page()

    # 3输入网址
    page.goto(url=url,wait_until='domcontentloaded')

    # 4查询条件为爬虫
    # 输入查询条件
    page.fill('[placeholder="搜索职位、公司或地点"]','爬虫')

    # 5.点击查询
    page.evaluate('$("#search_button").click()')
    time.sleep(5)
    # 6.等待页面加载
    page.wait_for_load_state(timeout=5000)
    # 7找到所在标签
    s=page.inner_html('id=jobList')

    # 获取当前页的职位名称，薪资，地区的数据
    # 8保存到本地
    # 将以上数据写入到html文件中
    with open('lagou.html','w',encoding='utf-8')as f:
        f.write(s)
    page.close()
    chrom.close()

    # 6．以合理的方式解析html文件，转存为json文件
    # 7．读取json文件，将数据存储到mongodb数据库中，字段与json文件的key对应
    # 8．查询上述数据库中薪资最大的职位名称

def to_mongodb():
    soup=BeautifulSoup(open('lagou.html',encoding='utf-8'),'lxml')
    div_all=soup.find_all(name='div',class_='item__10RTO')
    res=[]
    for i in div_all:
        lt=list(i.stripped_strings)
        dict1={
            'name':lt[0].split('[')[0],
            'city':re.findall('\[(.*?)\]',lt[0])[0],
            'max_salary':int(lt[2].split('-')[1].rstrip('k')),
            'min_salary':int(lt[2].split('-')[0].rstrip('k'))
        }
        res.append(dict1)
    with open('res.json','w',encoding='utf-8')as f:
        f.write(json.dumps(res))
    table.delete_many({})
    table.insert_many(res)
def get_one():
    info=table.find().sort('max_salary',-1)
    print(list(info)[0])

if __name__ == '__main__':
    # 使用playwright访问拉钩招聘https: // www.lagou.com /，获取指定信息
    url='https://www.lagou.com/'

    # 2．使用内置的任意浏览器访问该网站
    # with sync_playwright() as p:
    #     run(p,url)

    to_mongodb()

    get_one()