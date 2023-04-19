from flask import Flask,jsonify,request,render_template
from utils.db_client import Mongodb
import pandas as pd
from pyecharts.charts import Pie
app = Flask(__name__)

# 10.定义一个接口，获取30天的所有天气详情
@app.route('/get_30')
def hello_world():  # put application's code here
    # 11.
    # 需要支持最高气温或者时间的排序功能
    cs=request.form.get('cs')
    info=Mongodb.table.find().sort(cs,-1)
    res_list=[]
    for i in info:
        dict={
            'date': i['date'],
            'week': i['week'],
            'weather': i['weather'],
            'min_wen': i['min_wen'],
            'max_wen': i['max_wen']
        }
        res_list.append(dict)
    return jsonify(res_list)



# 12.定义一个接口，实现获取指定日期的天气详情
# 13.需要对传入的日期做数据校验
@app.route('/get_date')
def get_date():
    date=request.form.get('date',None)
    if date:
        info=Mongodb.table.find({'date': date})
        info_list=[]
        for i in info:
            x_dict={
                'date': i['date'],
                'week': i['week'],
                'weather': i['weather'],
                'min_wen': i['min_wen'],
                'max_wen': i['max_wen']
            }
            info_list.append(x_dict)
        return jsonify(info_list)
    else:
        return jsonify({'msg':'日期格式错误'})




# 14.定义一个接口，实现获取指定日期范围内的天气详情
# 15.需要支持分页功能
@app.route('/get_date_page')
def get_date_page():
    s_date=request.form.get('s_date')
    e_date = request.form.get('e_date')
    page=int(request.form.get('page'))

    info=Mongodb.table.find({
        'date':
            {'$gte': s_date, '$lte': e_date}}
    ).skip((page-1)*2).limit(2)

    info_list = []
    for i in info:
        x_dict = {
            'date': i['date'],
            'week': i['week'],
            'weather': i['weather'],
            'min_wen': i['min_wen'],
            'max_wen': i['max_wen']
        }
        info_list.append(x_dict)
    return jsonify(info_list)

# 16.定义一个接口，实现获取指定天气情况的天气日期以及对应的星期
# 17.需要判断传过来的数据是否合法，目前只支持多云，晴，阴等
@app.route('/get_one')
def get_one():
    state=request.form.get('state')
    state_list=['多云','晴','阴']
    if state not in state_list:
        return jsonify({'msg':'数据不合法'})
    info = Mongodb.table.find({'weather':state})
    info_list = []
    for i in info:
        x_dict = {
            'date': i['date'],
            'week': i['week'],
            'weather': i['weather'],
            'min_wen': i['min_wen'],
            'max_wen': i['max_wen']
        }
        info_list.append(x_dict)
    return jsonify(info_list)
# 18.定义一个接口，获取晴天，阴天，多云，雨天在30天中的占比情况
# 19.上述占比情况需要使用饼图进行可视化展示
@app.route('/get_19')
def get_19():
    info = Mongodb.table.find()
    info_list = []
    for i in info:
        x_dict = {
            'date': i['date'],
            'week': i['week'],
            'weather': i['weather'],
            'min_wen': i['min_wen'],
            'max_wen': i['max_wen']
        }
        info_list.append(x_dict)
    df=pd.DataFrame(info_list)
    df=df[df['weather'].isin(['晴天','阴天','多云','雨天'])]
    df=df.groupby(by='weather').count()
    pie=(
        Pie()
        .add('占比情况',list(zip(df.index.tolist(),df.values.tolist())))
    )
    pie.render('templates/19.html')
    return render_template('19.html')


if __name__ == '__main__':
    app.run(debug=True)
