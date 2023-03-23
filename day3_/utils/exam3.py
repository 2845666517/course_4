import requests
import re
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 访问网址如下：http://www.gov.cn/zhengce/zuixin.htm
    url = 'http://www.gov.cn/zhengce/zuixin.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }

    # 爬取上述网站，获取可以正确解码的数据
    # res=requests.get(url=url,headers=headers)
    # res.encoding='utf-8'

    # 将以上数据保存到本地，方便后续数据分析
    # with open('exam3.html','w',encoding='utf-8')as f:
    #     f.write(res.text)

    # 期望输出：
    # 1．获取到文件中title标签中的内容
    soup=BeautifulSoup(open('exam3.html',encoding='utf-8'),'lxml')
    # print(soup.title.text)

    # 2．用正则表达式匹配所有包含"content"单词的链接
    a_all=soup.find_all(name='a')
    a_list=[]
    text_list=[]
    for i in a_all:
        if re.findall('content',i['href']):
            a_list.append(i['href'])
        # 3．提取链接和文本信息，存放到字典中，格式自定义
        a_dict={
            i.text:i['href']
        }
        text_list.append(a_dict)
    # print(a_list)
    # print(text_list)

    # 4．获取国务院关于同意在北京设立国家植物园的批复这条信息的发布时间
    div_a=soup.find(name='div',class_='list list_1 list_2')
    li_all=div_a.find_all(name='li')
    for i in li_all:
        info = list(i.stripped_strings)
        if info=='国务院关于同意在北京设立国家植物园的批复':
            print(info[-1])


