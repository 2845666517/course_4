from flask import Flask,jsonify,request,session,make_response,render_template
from utils.models import College
import pandas as pd
from pyecharts.charts import Bar,Pie,WordCloud,Line


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/get_all_list')
def get_all_list():
    name=request.form.get('name')
    page=int(request.form.get('page',1))
    page_size=int(request.form.get('page_size',5))
    filter_list=[]
    if name!=None:
        filter_list.append(College.school.like(f'%{name}%'))
    # 根据条件查询
    info=College.query.filter(*filter_list).order_by(College.rank).offset((page-1)*page_size).limit(page_size).all()
    res_lt=[]
    for i in info:
        a=i.to_json()
        res_lt.append(a)
    # 8.
    # 接口数据必须使用JSON格式进行返回
    return jsonify(res_lt)

@app.route('/get_list')
def get_list():
    # 13.
    # 定义接口get_list，通过参数获取指定省市的总分的平均值以及对应的所有学校的详细信息
    sheng=request.form.get('sheng')
    info=College.query.filter(College.address==sheng).all()
    res_lt = []
    sum_score=0
    for i in info:
        a = i.to_json()
        res_lt.append(a)
        sum_score+=float(a['sum_score'])
    return jsonify({'msg':res_lt,'sum_score':round(sum_score,2)})


def get_df():
    info=College.query.all()
    res_lt = []
    for i in info:
        a = i.to_json()
        res_lt.append(a)
    return res_lt


# 14.定义接口get_word，生成学校名称的词云图
@app.route('/get_word')
def get_word():
    df=pd.DataFrame(get_df())
    df15=df.groupby('school')['id'].count()
    word=(
        WordCloud()
        .add('',list(zip(df15.index.tolist(),df15.values.tolist())))
    )
    word.render('./templates/14.html')
    return render_template('14.html')

# 15.定义接口get_pie，获取各个省市的学校占比情况，实现饼图效果
@app.route('/get_pie')
def get_pie():
    df=pd.DataFrame(get_df())
    df15=df.groupby('address')['id'].count()
    pie=(
        Pie()
        .add('',list(zip(df15.index.tolist(),df15.values.tolist())))
    )
    pie.render('./templates/15.html')
    return render_template('15.html')

# 16.定义接口get_bar，获取各个学校的指标得分的情况，使用柱状图可视化展示
@app.route('/get_bar')
def get_bar():
    df = pd.DataFrame(get_df())
    df15 = df.groupby('school')['id'].count()
    bar=(
        Bar()
        .add_xaxis(df15.index.tolist())
        .add_yaxis('',df15.values.tolist())
    )
    bar.render('./templates/16.html')
    return render_template('16.html')

# 17.定义接口get_line，获取各个省市的总分的最大值，总分的最小值，生成多维折线图
@app.route('/get_line')
def get_line():
    df = pd.DataFrame(get_df())
    df15 = df.groupby('address')['sum_score'].sum()
    bar = (
        Bar()
        .add_xaxis(df15.index.tolist())
        .add_yaxis('', df15.values.tolist())
    )
    bar.render('./templates/17.html')
    return render_template('17.html')

# 18.定义接口get_index，将上述的14,  15，16，17题的数据通过数据大屏展示
@app.route('/get_index')
def get_index():
    return render_template('screen.html')


if __name__ == '__main__':
    app.run()
