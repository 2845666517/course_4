import requests
from flask import Flask,jsonify
from sqlalchemy.engine import create_engine

app = Flask(__name__)

url='http://www.ini5.com/i15973.html'
DB_RUL='mysql+pymysql://root:root@127.0.0.1:3306/3_21?charset=utf8'
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
}
engine=create_engine(DB_RUL)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('./')
def set_html():
    res=requests.get(url=url,headers=headers)
    with open('res.html','w',encoding='utf-8')as f:
        f.write(res.text)

    # 存入数据库

    return jsonify({'msg':'成功'})



if __name__ == '__main__':
    app.run(debug=True)
    # 使用flask搭建接口1，2
    # 实现爬取网站中的文本内容，并将其返回
    # 接口1读取上述的文本内容，进行提取信息，期望输出排名，国家，GDP的值（推荐使用字典的格式）
    # 接口2将上述的字典格式数据，写入到本地的mysql中，表自定义
    # 分别使用postman对以上接口进行测试并输出对应信息以及注释

