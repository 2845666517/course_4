import requests
from bs4 import BeautifulSoup
from utils.db_client import Mongodb


headers={
    'Referer': 'https://www.tianqi.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
}
def save_html():
    url = 'https://www.tianqi.com/beijing/30/'
    res = requests.get(url=url, headers=headers)
    # 保存文件
    with open('./data/res.html', 'w', encoding='utf-8') as f:
        f.write(res.text)

def save_icon(soup):
    div_all=soup.find_all(name='div',class_='weaul_a')
    for j,i in enumerate(div_all):
        img_url='https:'+i.find(name='img')['src']
        img=requests.get(url=img_url,headers=headers)
        with open(f'../static/{j}.png','wb')as f:
            f.write(img.content)

def save_sql(soup):
    ul_a=soup.find(name='ul',class_='weaul')
    li_all=ul_a.find_all(name='li')
    Mongodb.table.drop()
    for i in li_all:
        i_list=list(i.stripped_strings)
        i_dict={
            'date':i_list[0],
            'week':i_list[1],
            'weather':i_list[2],
            'min_wen':i_list[3],
            'max_wen': i_list[5]
        }
        Mongodb.table.insert_one(i_dict)


if __name__ == '__main__':
    # 保存网页
    # save_html()

    # 解析html
    soup = BeautifulSoup(open('./data/res.html', encoding='utf-8'), 'lxml')
    # save_icon(soup)

    # 保存到数据库
    save_sql(soup)