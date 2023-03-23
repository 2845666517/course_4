from flask import Flask,jsonify
import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
DB_URI='mysql+pymysql://root:root@127.0.0.1:3306/3_21?charset=utf8'
engine=create_engine(DB_URI)
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
@app.route('/save_html')
def save_html():
    url='https://www.phb123.com/hangye/qiche/CN.html'
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    }
    res=requests.get(url,headers=headers)
    with open('res.html','w',encoding='utf-8')as f:
        f.write(res.text)

    df=pd.read_html('res.html')[0]
    df.to_sql('cars',con=engine,if_exists='replace')
    return jsonify({'msg':'保存成功'})


@app.route('/read_sql')
def read_sql():
    df=pd.read_sql('SELECT * FROM cars',con=engine)
    res=df.to_dict('records')
    return jsonify({'msg':res})

if __name__ == '__main__':
    app.run(debug=True)
