import pandas
from flask import Flask,request,session,current_app,make_response,Blueprint,jsonify,render_template
from pyecharts.charts import Bar,Pie,Line,WordCloud
from utils.db_client import Mongodb
import pandas as pd

homes=Blueprint('homes',__name__,url_prefix='/homes')

# 7.编写一个接口get_all_house，获取所有房源的详细信息 (2分)
# 8.该接口需支持根据房源面积排序(3分)
# 9.该接口需支持分页展示数据(3分)
# 10.该接口需支持根据小区的名称模糊查询(3分)
@homes.route('/get_all_house')
def get_all_house():
    name=request.form.get('name')
    area=request.form.get('area')
    page=int(request.form.get('page',1))
    page_size = int(request.form.get('page_size',2))
    if area:
        info=Mongodb.table.find({'name':{'$regex':name}})\
            .sort(area,1).skip((page-1)*page_size).limit(page_size)
    else:
        info = Mongodb.table.find({'name': {'$regex': name}}).skip((page - 1) * page_size).limit(page_size)
    res_lt=[]
    for lt in info:
        dict1 = {
            'title':lt['title'],
            # 小区名称
            'name':lt['name'],
            # 房源地址
            'address':lt['address'],
            # 小区面积
            "area":lt['area'],
            # 装修
            'style':lt['style'],
            # 关注
            'people':lt['people'],
            # 单价
            'money_one':lt['money_one'],
            # 总价
            'money_all':lt['money_all']
        }
        res_lt.append(dict1)
    return jsonify(res_lt)

# 11.编写接口get_house_name根据的小区名称获取房源的具体数据 (2分)
# 12.以上接口需使用Mongodb来查询(2分)
@homes.route('/get_house_name')
def get_house_name():
    name=request.form.get('name')
    info=Mongodb.table.find({'name':name})
    res_lt = []
    for lt in info:
        dict1 = {
            'title': lt['title'],
            # 小区名称
            'name': lt['name'],
            # 房源地址
            'address': lt['address'],
            # 小区面积
            "area": lt['area'],
            # 装修
            'style': lt['style'],
            # 关注
            'people': lt['people'],
            # 单价
            'money_one': lt['money_one'],
            # 总价
            'money_all': lt['money_all']
        }
        res_lt.append(dict1)
    return jsonify(res_lt)

# 13.把mongodb的数据转换成pandas的数据格式(2分)
# 15.数据分批取出,转换成dataframe格式的(2)
# 16.把数据合并成一个dataframe 根据情况使用 merge,concat合并方式(4)
def get_df():
    dfa=pd.DataFrame(Mongodb.table.find().limit(20))
    dfb = pd.DataFrame(Mongodb.table.find().skip(20))
    df=pd.concat((dfa,dfb),axis=0)
    df.drop('_id',inplace=True,axis=1)
    return df


# 14.编写接口统计小区的房源数量,使用pyechars可视化展示 柱状图(3分)
@homes.route('/get_house_num')
def get_house_num():
    df=get_df()
    df1=df.groupby('name')['title'].sum()
    bar=(
        Bar()
        .add_xaxis(df1.index.tolist())
        .add_yaxis('',df1.values.tolist())
    )
    bar.render('./templates/16.html')
    return render_template('16.html')

# 17.定义flask接口，统计关注人数大于3人的二手房装修风格,选取次数最多的前100个,词云图展示(4分)
@homes.route('/get_house_3')
def get_house_3():
    df=get_df()
    df1=df[df['people']>3]
    df17=df1.groupby(by='style')['title'].count()
    word=(
        WordCloud()
        .add('',list(zip(df17.index.tolist(),df17.values.tolist())))
    )
    word.render('./templates/17.html')
    return render_template('17.html')


# 18.定义flask接口，获取各个房源装修的占比情况，实现饼图效果(4分)
@homes.route('/get_house_pie')
def get_house_pie():
    df=get_df()
    df18=df.groupby(by='address')['title'].sum()
    pie=(
        Pie()
        .add('',list(zip(df18.index.tolist(),df18.values.tolist())))
    )
    pie.render('./templates/18.html')
    return render_template('18.html')


# 19.统计每个区域的房源数量,折线图展示(4分)
# 20..使用cut根据面积分区间组0 - 30, 31 - 60, 61 - 60, 91 - 120, 120以上t统计他们的分布情况 柱状图展示(4分)
# 21.定义flask接口，将上述的19.20，21,22题的数据通过数据大屏展示(4分)
# 22.使用合适的算法分析二手房面积分布于价格的关系（4分）
