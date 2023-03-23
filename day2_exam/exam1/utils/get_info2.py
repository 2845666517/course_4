import re
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url='http://www.gov.cn/xinwen/2022-01/06/content_5666644.htm'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }
    # res=requests.get(url=url,headers=headers)
    # res.encoding='utf-8'
    # with open('exam2.html','w',encoding='utf-8')as f:
    #     f.write(res.text)


    # 获取左侧logo下的内容图片信息，存入到本地img目录中
    soup=BeautifulSoup(open('exam2.html',encoding='utf-8'),'lxml')
    url_img='http://www.gov.cn/govweb/xhtml/2016gov/images/public/logo.jpg'
    # res2=requests.get(url=url_img,headers=headers)
    # with open('exam2.png','wb')as f:
    #     f.write(res2.content)

    bag_all=soup.find(name='div',class_='BreadcrumbNav')
    lt=[]
    for i in bag_all:
        lt.append(i.text)
    # print(lt)

    id_a=soup.find(name='div',id='UCAP-CONTENT')
    p_all=soup.find_all(name='p')
    lt2=[]
    for i in p_all:
        lt2.append(i.text)
    # print(lt2)

    all=soup.find_all(class_=re.compile("share"))
    for i in all:
        print(i.text)
    a='123'.find('5')
    print(a)