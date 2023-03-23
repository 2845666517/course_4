from flask import Flask,jsonify
import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine

app = Flask(__name__)

url='http://www.ini5.com/i15973.html'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
}

DB_URI=f'mysql+pymysql://root:root@127.0.0.1:3306/3_21?charset=utf8'
engine=create_engine(DB_URI)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/save_html')
def save_html():
    res=requests.get(url=url,headers=headers)
    with open('res.html','w',encoding='utf-8')as f:
        f.write(res.text)
    return jsonify({'msg':'保存网页成功'})


@app.route('/save_sql')
def save_sql(path='res.html'):
    # 把html解析成bs4可以解析的对象
    soup=BeautifulSoup(open(path,encoding='utf-8'),'lxml')
    # 获取所要数据的标签
    div_a=soup.find(name='div',class_='detail_article')
    p_all=div_a.find_all('p')
    res=[]
    for p in p_all[2:-1]:
        p_list=list(p.stripped_strings)
        p_dict={
            '排名':p_list[0].split('、')[0],
            '国家':p_list[0].split('，')[0].split('是')[-1],
            'gdp':p_list[0].split('，')[1].split('为')[-1]
        }
        res.append(p_dict)

    # 表
    df=pd.DataFrame(res)
    df.to_sql('gdp',con=engine)
    return jsonify({'data':res})



if __name__ == '__main__':
    app.run(debug=True)
