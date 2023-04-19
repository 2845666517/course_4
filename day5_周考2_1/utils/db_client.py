import pymongo
class Mongodb():
    client=pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )
    # 创建数据库
    db=client['2010A_w2_1']
    # 创建表
    table=db['2010A_w2_1']
    