import pandas as pd
from flask import Flask,jsonify,request,render_template
from utils.db_client import Pymongo
from pyecharts.charts import *

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# 11.以下接口需要以JSON格式进行返回
# 12.定义一个接口，获取所有作家的详细信息
# 13.支持姓名或者朝代的模糊匹配
# 14.支持分页功能
@app.route('/get_all')
def get_all():
    name=request.form.get('name')
    cd=request.form.get('cd')
    page=int(request.form.get('page',1))
    filter_list=[]
    if name!=None:
        filter_list.append({'作家姓名：':{'$regex':name}})
    if cd!=None:
        filter_list.append({'朝代：': {'$regex': cd}})

    info=Pymongo.table2.find({'$or':filter_list}).skip((page-1)*2).limit(7)

    res=[]
    for i in info:
        i.pop('_id')
        res.append(i)
    return jsonify(res)

# 15.定义一个接口，获取指定朝代的作家的详细信息
@app.route('/get_cd')
def get_cd():
    cd=request.form.get('cd')
    info=Pymongo.table2.find({'朝代：': cd})
    res=[]
    for i in info:
        i.pop('_id')
        res.append(i)
    return jsonify(res)

# 16.定义一个接口，统计各个朝代的作家的占比情况，以饼图进行可视化展示
@app.route('/get_16')
def get_16():
    df=pd.DataFrame(Pymongo.table2.find())
    df=df.groupby(by='朝代：')['作家姓名：'].count()
    pie=(
        Pie()
        .add('',list(zip(df.index.tolist(),df.values.tolist())))
    )
    pie.render('templates/16.html')
    return render_template('16.html')

# 17.定义一个接口，获取公元后出生的作家的详细信息
@app.route('/get_gongyuan')
def get_gongyuan():
    info=Pymongo.table2.find({'出生': '公元后'})
    res=[]
    for i in info:
        i.pop('_id')
        res.append(i)
    return jsonify(res)




# 18.定义一个接口，统计每个朝代的出生在公元前后的作家的数量，以多维柱状图进行可视化展示
@app.route('/get_18')
def get_18():
    df=pd.DataFrame(Pymongo.table2.find())
    df=df.groupby(by=['朝代：','出生'])['作家姓名：'].count()
    print(df)
    bar=(
        Bar()
        .add_xaxis(df.index.tolist())
        .add_yaxis('',df.index.tolist())
        .add_yaxis('',df.values.tolist())
    )
    bar.render('templates/18.html')
    return render_template('18.html')




# 19.定义一个接口，统计各个籍贯下的作家的总数，以折线图进行可视化展
@app.route('/get_19')
def get_19():
    df=pd.DataFrame(Pymongo.table2.find())
    df=df.groupby(by='籍贯：')['作家姓名：'].count()
    print(df)
    line=(
        Line()
        .add_xaxis(df.index.tolist())
        .add_yaxis('',df.values.tolist())
    )
    line.render('templates/19.html')
    return render_template('19.html')

if __name__ == '__main__':
    app.run()
