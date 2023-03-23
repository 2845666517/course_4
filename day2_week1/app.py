import pandas as pd
from flask import Flask,request,jsonify
import requests
from bs4 import BeautifulSoup
from utils.Mysql import init_db
from utils.Mysql import engine

app = Flask(__name__)
from package.blueprint.asia import asia
app.register_blueprint(asia)
from package.blueprint.fbs import fbs
app.register_blueprint(fbs)

url1='https://www.phb123.com/renwu/fuhao/shishi.html'
url2='https://www.phb123.com/renwu/fuhao/zhou_AS.html'
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
}

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/initdb')
def initdb():
    init_db()
    return '完成'

@app.route('/save_html')
def save_html():
    res1=requests.get(url=url1,headers=headers)
    res1.encoding='utf-8'
    res2 = requests.get(url=url2, headers=headers)
    res2.encoding = 'utf-8'
    with open('templates/res1.html','w',encoding='utf-8')as f:
        f.write(res1.text)
    with open('templates/res2.html','w',encoding='utf-8')as f:
        f.write(res2.text)
    return jsonify({'msg':'保存完成'})

@app.route('/save_sql1')
def save_sql1():
    df=pd.read_html('templates/res1.html')[0]
    df['财富(10亿美元)']=df['财富(10亿美元)'].apply(lambda x: float(x.split('亿')[0]))
    df.to_sql('fbs',con=engine,if_exists='replace',index=Flask)
    return jsonify({'msg':'保存成功'})

@app.route('/save_sql2')
def save_sql2():
    df=pd.read_html('templates/res2.html')[0]
    df['财富(10亿美元)']=df['财富(10亿美元)'].apply(lambda x: float(x.split('亿')[0]))
    df.to_sql('asia',con=engine,if_exists='replace',index=Flask)
    return jsonify({'msg':'保存成功'})

if __name__ == '__main__':
    app.run(debug=True)
