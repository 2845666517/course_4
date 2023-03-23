from flask import Blueprint,request,session,jsonify
import pandas as pd
from utils.Mysql import engine
fbs=Blueprint('fbs',__name__,url_prefix='/fbs')
df = pd.read_sql('select * from fbs', con=engine)


@fbs.route('/')
def index():
    return 'fbs'




# 15.定义接口get_fuhao_list，读取福布斯排行榜，获取所有的福布斯实时富豪榜中的数据
@fbs.route('/get_fuhao_list')
def get_fuhao_list():
    return jsonify({'msg': df.to_dict('records')})

# 16.定义接口get_usa_count，读取福布斯排行榜，获取美国下富豪的人数
@fbs.route('/get_usa_count')
def get_usa_count():
    df_new=df.loc[df[df['国家/地区']=='美国'].index,:]
    return jsonify({'人数': len(df_new)})

# 17.定义接口get_top1000_list，读取福布斯排行榜，获取财富大于1000亿美元的各个国家的占比情况
@fbs.route('/get_top1000_list')
def get_top1000_list():
    df_new=df.loc[df[df['财富(10亿美元)']>1000].index,:]
    return jsonify(df_new)

# 18.定义接口get_source_name，读取福布斯排行榜，根据财富来源，生成对应的词云图，并返回
# 19.定义接口get_country_money，读取福布斯排行榜，获取所有的国家的总财富，以及富豪人数，生成多维柱状图，并返回
