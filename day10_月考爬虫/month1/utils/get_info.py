import requests,os
from bs4 import BeautifulSoup
import threading
from db_client import Mongodb

headers={
    'Referer': 'https://bj.lianjia.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
}

def get_html(url,page):
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    # 保存网页
    with open(f'./data/html/{page}.html','w',encoding='utf-8')as f:
        f.write(res.text)

    soup = BeautifulSoup(res.text, 'lxml')
    div_all = soup.find_all(name='div', class_='info clear')
    res_lt = []
    for i in div_all:
        lt = list(i.stripped_strings)
        dict = {
            'title': lt[0],
            # 小区名称
            'name': lt[2],
            # 房源地址
            'address': lt[4],
            # 小区面积
            "area": float(str(lt[5]).split(' | ')[1].split('平米')[0]),
            # 装修
            'style': str(lt[5]).split(' | ')[3],
            # 关注
            'people': lt[-7].split('人关注')[0],
            # 单价
            'money_one': float(lt[-1][3:].replace(',', '')),
            # 总价
            'money_all': lt[-3]
        }
        res_lt.append(dict)
    Mongodb.table.insert_many(res_lt)


    ul_a = soup.find(name='ul', class_='sellListContent')
    img_all = ul_a.find_all(name='img', class_='lj-lazy')
    # 多线程保存图片
    for i, j in enumerate(img_all):
        img_content=requests.get(url=j['data-original'],headers=headers)
        with open(f'./data/images/{page}_{i+1}.png','wb')as f:
            f.write(img_content.content)



def save_html():
    url_list=[f'https://bj.lianjia.com/ershoufang/pg{i}/' for i in range(1,21)]
    # 4.根据下面的需求爬取房源数据,使用多任务爬取1-20页的数据 (8分)
    Mongodb.table.delete_many({})
    # ['世纪星城带电梯顶层复式 楼上没有算房本面积', '必看好房', '世纪星城', '-', '通州北苑',
    #  '4室2厅 | 92.2平米 | 南 北 | 简装 | 高楼层(共10层) | 2005年建 | 板楼', '59人关注 / 5个月以前发布', 'VR房源',
    #  '房本满五年', '随时看房', '550', '万', '59,653元/平', '关注', '加入对比']
    for i,j in enumerate(url_list):
        thread=threading.Thread(target=get_html,args=([j,i+1]))
        thread.start()






    # 5.把数据保存到MongoDB中(5分)
if __name__ == '__main__':
    # a=input('是否爬网页？1，2')
    # if a=='1':
    save_html()
