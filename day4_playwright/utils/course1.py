import os
import threading
import time,random,pandas
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import threading


def run(p):
    # """
    # 1:找到浏览器
    chrom=p.chromium.launch(headless=False)

    # 2:打开浏览器
    page=chrom.new_page()

    """
    dom:文本
    content:内容
    loaded:加载
    """
    # 3:去网址
    page.goto('https://www.lagou.com/',wait_until='domcontentloaded')

    # 4:输入查询条件
    page.fill('[placeholder="搜索职位、公司或地点"]','python')

    # 5点击查询
    page.evaluate('$("#search_button").click()')

    # 6:等待页面数据加载
    page.wait_for_load_state(timeout=10000)

    # 7:找到数据所在标签
    # 8:标签保存到本地
    for i in range(1,11):
        t=random.randint(1,5)
        s = page.inner_html('id=jobList')
        with open(f'./data/res{i}.html','w',encoding='utf-8')as f:
            f.write(s)
        page.click('text=下一页')
        time.sleep(t)

    # 关闭网站
    page.close()

    # 关闭浏览器
    chrom.close()

# 保存的网页操作
def get_one(path):
    soup=BeautifulSoup(open(path,encoding='utf-8'),'lxml')
    div_all=soup.find_all(name='div',class_='item__10RTO')
    res=[]
    for i in div_all:
        lt=list(i.stripped_strings)
        dict1={
            'name':lt[0].split('[')[0],
            'city':lt[0].split('[')[-1].split('·')[0],
            'max_money':int(lt[2].split('-')[-1].rstrip('k')),
            'min_money': int(lt[2].split('-')[0].rstrip('k')),
            'jinyan':lt[3].split('/')[0],
            'xueli':lt[3].split('/')[-1],
            'conpany':lt[4]
        }
        res.append(dict1)
    df=pandas.DataFrame(res)
    print(df)

if __name__ == '__main__':
    # 获取数据
    with sync_playwright() as p:
        run(p)

    # 网页操作
    # htmls=os.listdir('data')
    # for i in htmls:
    #     thread=threading.Thread(target=get_one,args=[f'./data/{i}'])
    #     thread.start()
