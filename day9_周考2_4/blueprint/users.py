import datetime
from flask import Blueprint,request,jsonify,render_template,redirect
from hashlib import md5
import jwt
from functools import wraps
import utils.db_client
from utils.db_client import Mongodb
users=Blueprint('users',__name__,url_prefix='/users')

users.route('/')
def index():
    return 'ok'


def encode_password(password):
    return md5(password.encode(encoding='utf-8')).hexdigest()
@users.route('/register',methods=['post'])
def register():
    username=request.form.get('username')
    password=request.form.get('password')
    role=request.form.get('role','普通')

    dict1={
        'username':username,
        'password':encode_password(password),
        'role':role
    }
    Mongodb.users.insert_one(dict1)
    return jsonify({'msg':'注册成功'})


@users.route('/login',methods=['post'])
def login():
    username=request.form.get('username')
    password=request.form.get('password')

    # 数据验证
    res=Mongodb.users.find_one({'username':username})
    if not res:
        return jsonify({'msg':'未注册过'})

    if res['password']!=encode_password(password):
        return jsonify({'msg':'登录失败'})
    # 9.JWT的有效期为5分钟
    token=jwt.encode(
        {username:password,'exp':datetime.datetime.now()+datetime.timedelta(minutes=5)}
    )
    return jsonify({'msg':'登录成功'})

@users.route('/loginout',methods=['post'])
def loginout():
    username=request.form.get('username')
    Mongodb.users.delete_one({"username":username})
    return jsonify({'msg':'登出成功'})


# 18.实现一个添加课程的接口,该接口只有管理员才可以访问
@users.route('/add_course',methods=['post'])
def add_course():
    course_name=request.form.get('course_name')
    user=request.form.get('user')
    Mongodb.courses.insert_one({'course_name':course_name,'user':user})
    return jsonify({'msg':'添加成功'})


#管理员 装饰器
def checke_admin(fn):
    @wraps(fn)
    def inner():
        user=Mongodb.users.find_one()
        if user['role']!='admin':
            return jsonify({'msg':'不是管理员'})
        fn()
    return inner


# 普通用户装饰器




# 19.实现一个查看所有课程的接口,该接口只有普通用户才可以访问
@users.route('/look_all',methods=['post'])
def look_all():
    info=Mongodb.courses.find()
    res=[]
    for i in info:
        i.pop('_id')
        res.append(i)
    return jsonify(res)