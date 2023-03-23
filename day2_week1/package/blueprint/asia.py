from flask import Blueprint,request,session,jsonify
from utils.models import Asia,FBS
from utils.Mysql import engine
import pandas as pd
asia=Blueprint('asia',__name__,url_prefix='/asia')

@asia.route('/')
def index():
    return 'asis'

# 13.定义接口get_asia_list，读取亚洲排行榜，获取所有的亚洲富豪排行榜的数据
@asia.route('/get_asia_list')
def get_asia_list():
    df=pd.read_sql('select * from asia',con=engine)
    print(df)
    return jsonify({'msg':df.to_dict('records')})

# 14.定义接口get_china_list，读取亚洲排行榜，获取所有的中国富豪排行榜的数据
@asia.route('/get_china_list')
def get_china_list():
    res=pd.read_sql('fbs',con=engine).to_dict('records')
    print(res)
    new_res=[]
    for i in res:
        if i['国家/地区']=='中国':
            new_res.append(i)
    return jsonify(new_res)
