from flask import Flask,request,jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/hello',methods=['Get'])
def hello():
    name=request.args.get('name')
    classes = request.args.get('classes')
    dict={name:classes}
    print(dict)
    return jsonify(dict)
@app.route('/add',methods=['post'])
def add():
    name = request.form.get('name')
    classes = request.form.get('classes')
    dict = {name: classes}
    print(dict)
    return jsonify(dict)

if __name__ == '__main__':
    """
    1．简单搭建flask框架
    2．实现两个接口，/hello  GET请求   /add   POST请求
    3．hello返回json数据，数据自定义，接收请求过来的数据，并打印
    4．add返回json数据，数据自定义，接收请求过来的数据，并打印
    5．使用requests访问hello接口，传参为自己的姓名，班级信息
    6．使用requests访问add接口，传参为自己的姓名，班级信息
    7．分别打印上述两个返回值response
    8．获取response的状态码，以及文本信息，url地址，json解析后的数据
    9．添加必要的注释
    10．代码命名合理规范
"""
    app.run()
