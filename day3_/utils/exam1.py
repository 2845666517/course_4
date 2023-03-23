import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    # 1．导入相关三方库
    url='https://item.jd.com/4645290.html'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }
    # res=requests.get(url=url,headers=headers)
    # res.encoding='utf-8'

    # 2．爬取上述网站，查看响应状态码
    # print(res.encoding)

    # 3．获取响应体编码
    # print(res.status_code)

    # 4．将上述的文本信息写入到当前文件下的4645290.html文件中
    # with open('4645290.html','w',encoding='utf-8')as f:
    #     f.write(res.text)

    # 5．采用合适的解析器去分析该html
    soup=BeautifulSoup(open('4645290.html',encoding='utf-8'),'lxml')

    # 6．获取到文件中title标签中的内容
    print(soup.title.text)

    # 7．获取<ul class="lh">子标签li中的所有img的src的信息，存放到列表中
    ul_a=soup.find(name='ul',class_='lh')
    li_all=ul_a.find_all(name='li')
    img_src=[]
    for i in li_all:
        img_all=i.find_all(name='img')
        for j in img_all:
            img_src.append(j['src'])
    print(img_src)

    # 8．获取a标签文本信息为’荣耀 V9 全网通 高配版 6GB+64GB 幻夜黑 移动联通电信4G手机 双卡双待‘ 的href的值
    a_all=soup.find_all(name='a')
    for i in a_all:
        if i.text=='荣耀 V9 全网通 高配版 6GB+64GB 幻夜黑 移动联通电信4G手机 双卡双待':
            a_herf = i['href']
            print(a_herf)
    # 9．添加必要的注释
    # 10．代码命名合理规范
