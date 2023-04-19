import random
import time
import threading
import requests
from bs4 import BeautifulSoup
# 互斥锁
lock=threading.Lock()
#模拟浏览器头部
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }


# 保存html文件
def save_html():
    # 首页
    index_page='https://wallhaven.cc/toplist?page=2'
    print('输入1则爬取首页图片')
    url = input('请输入要爬取图片的网址：')
    # 当url==1时爬取首页图片
    url=index_page
    # 开始保存网站内容
    res=requests.get(url=url,headers=headers)
    with open('weaper.html', 'w', encoding='utf-8')as f:
        f.write(res.text)

def get_weaper():
    # 解析所有weaper标签中的图片链接数据
    soup = BeautifulSoup(open('weaper.html', encoding='utf-8'), 'lxml')
    # 定位到id==thumbs的div
    div = soup.find(name='div', id='thumbs')
    # 定位到ul
    ul = div.find(name='ul')
    # 找到所有的li标签
    li_all = ul.find_all(name='li')

    # 存储所有图片路径
    url_list = []
    # 遍历所有li寻找链接
    for i in li_all:
        # 找到所有a标签
        a = i.find_all(name='a')
        for j in a:
            # 如果a有href属性就保存到路径
            if j.has_attr('href'):
                # 跳到新网址
                res = requests.get(url=j['href'], headers=headers)
                # 解析新网址内容
                soup = BeautifulSoup(res.text, 'lxml')
                # 获取img的src路径
                wallpaper = soup.find(name='img', id='wallpaper')
                # 保存到url_list列表
                url_list.append(wallpaper['src'])
    print(f'所有图片路径{url_list}')


    # 爬取图片
    for j, i in enumerate(url_list):
        t = random.randint(2, 5)
        res = requests.get(url=i, headers=headers)
        print(f'爬取第{j + 1}张图片中……')
        print(f'地址{i}')
        with open(f'../data/img/{time.time()}.jpeg', 'wb') as f:
            f.write(res.content)
        print(f'爬取第{j + 1}张图片成功')
        print('等待2到5秒')
        # 睡眠2到5秒
        time.sleep(t)


if __name__ == '__main__':
    # 保存网页
    save_html()
    # 爬取图片
    get_weaper()

