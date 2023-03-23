import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 访问以下网站：https: // movie.douban.com / top250
    url='https://movie.douban.com/top250'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }

    # 使用合适的方法正确爬取上述网站
    # 响应体信息怎么保存，可以减少对网站的爬取压力
    # 如何对文本信息进行分析（提示：不要重复爬取网站）
    # res=requests.get(url=url,headers=headers)
    # res.encoding='utf-8'
    # with open('exam2.html','w',encoding='utf-8')as f:
    #     f.write(res.text)

    # 期望：
    # 1．获取到文件中title标签中的内容
    soup=BeautifulSoup(open('exam2.html',encoding='utf-8'),'lxml')
    print(soup.title.text)

    # 2．获取到所有a标签的href的值，存放到列表中
    a_all=soup.find_all(name='a')
    a_list=[]
    for i in a_all:
        a_list.append(i['href'])
    # print(a_list)

    # 3．top250电影名称的汇总
    ol_a=soup.find(name='ol',class_='grid_view')
    li_all=ol_a.find_all(name='li')
    movies_name=[]
    movies_list=[]

    for i in li_all:
        lt=list(i.stripped_strings)
        dict_movies={
            lt[1]:lt[-2]
        }
        movies_list.append(dict_movies)
        movies_name.append(lt[1])
    print(movies_name)
    print(movies_list)
    # 4．电影名称对应的电影评价次数，合理的方式存储
