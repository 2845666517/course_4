import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    # url = 'http://www.gov.cn/xinwen/2022-01/04/content_5666401.htm'
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    # }
    # res=requests.get(url=url,headers=headers)
    # res.encoding='utf8'
    # with open('exam3.html','w',encoding='utf-8')as f:
    #     f.write(res.text)

    soup=BeautifulSoup(open('exam3.html',encoding='utf-8'),'lxml')
    # title=soup.find(name='title').text+'.png'
    # img_src='http://www.gov.cn/xinwen/2022-01/04/'+soup.find(name='img',align='center')['src']
    # res=requests.get(url=img_src)
    # with open(title,'wb')as f:
    #     f.write(res.content)

    div_a=soup.find(name='li')
    print(div_a)
    # li_all=div_a.find_all(name='li')
    # print(li_all)
