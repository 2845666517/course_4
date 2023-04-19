import pymongo

class Mongodb:
    client=pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )
    db=client['users']
    users=db['users']#用户表
    courses=db['courses']#课程表
    stu=db['stu']#学生表