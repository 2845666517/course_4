# 1．导入连接MongoDB的python三方库
import pymongo

if __name__ == '__main__':
    # 2．启动本地MongoDB服务，保证运行正常，建立连接
    mogon=pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )
    # 3．创建数据库1908_1，创建数据集合1908_conn_1
    db=mogon['1908_1']
    table=db['1908_conn_1']

    # 4．往上述集合中插入数据
    # 数据如下：
    mylist = [ { "name": "Taobao", "alexa": "100", "url": "https://www.taobao.com" }, { "name": "QQ", "alexa": "101", "url": "https://www.qq.com" }, { "name": "Facebook", "alexa": "10", "url": "https://www.facebook.com" }, { "name": "知乎", "alexa": "103", "url": "https://www.zhihu.com" }, { "name": "Github", "alexa": "109", "url": "https://www.github.com" } ]
    table.insert_many(mylist)

    # 5．查看该集合中name的ASCII码大于等于b，alexa不等于100的数据
    print(table.find({'name':{'$gte':'b'},'alexa':{'$ne':100}}))

    # 6．修改alexa为100的数据，将name修改为淘宝
    table.update_one({'alexa':100},{'$set':{'name':'淘宝'}})
    print(list(table.find()))

    # 7．根据alexa进行降序排序
    print(list(table.find().sort('alexa',1)))

    # 8．删除所有的数据，以及删除数据集合
    table.delete_many({})
    db.drop_collection(table)
    mogon.drop_database(db)

    # 9．添加必要的注释
    # 10．代码命名合理规范