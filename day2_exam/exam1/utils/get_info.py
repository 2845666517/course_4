import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    # 2．爬取上述网站，获取响应体的编码以及响应体的文本信息
    url='http://www.gov.cn/zhengce/content/2021-12/29/content_5665109.htm'
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }
    # res=requests.get(url=url,headers=headers)

    # 3．修改编码为utf - 8，再次获取响应体的文本信息
    # res.encoding='utf-8'

    # 4．将上述的文本信息写入到当前文件下的content_5665109.html文件中
    # with open('content_5665109.html','w',encoding='utf-8')as f:
    #     f.write(res.text)

    # 5．获取到文件中title标签中的内容
    soup=BeautifulSoup(open('content_5665109.html',encoding='utf-8'),'lxml')
    print(soup.find(name='title').text)

    # 6．获取到所有p标签的内容，存放到字典中，格式自定义
    p_all=soup.find_all(name='p')
    dict6={}
    for i,j in enumerate(p_all):
        dict6[i]=j.text
    # print(dict6)

    # 7．获取到所有link标签中属性href的值，存放到列表中
    link_all=soup.find_all(name='link')
    lt7=[i['href'] for i in link_all]
    print(lt7)

    # 8．获取到所有a标签以及li标签的内容，存放到字典中，格式自定义
    a_all=soup.find_all(name=['a','li'])
    dict8={}
    for i,j in enumerate(a_all):
        dict8[i]=j.text
    print(dict8)

    # 9．添加必要的注释
    # 10．代码命名合理规范
