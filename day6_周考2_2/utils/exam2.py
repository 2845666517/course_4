import pymongo

if __name__ == '__main__':
    # 使用合适的库连接本地已经运行的mongodb，
    mongo=pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )

    # 建立连接后，创建一个数据库1908_1以及数据集合1908_conn_1，
    db=mongo['1908_1']
    table=db['1908_conn_1']

    # 将以下数据正确写入到集合中
    # 数据如下：
    document = [
        {'name': 'a', 'age': 18, 'sex': 'male'},
        {'name': 'b', 'age': 28, 'sex': 'male'},
        {'name': 'c', 'age': 15, 'sex': 'female'},
        {'name': 'd', 'age': 20, 'sex': 'male'},
        {'name': 'e', 'age': 24, 'sex': 'male'},
    ]
    table.insert_many(document)

    # 查看该集合中name的ASCII码大于等于b，age小于等于20，sex不等于female的数据

    res=table.find({'name':{'$gte':'b'},'age':{'$lte':20},'sex':{'$ne':'female'}})
    print(list(res))


    # 删除sex为female的数据
    table.delete_many({'sex':'female'})

    # 根据age进行升序排序
    print(list(table.find().sort('age',1)))

    # 删除所有的数据，以及删除数据集合
    table.delete_many({})
    db.drop_collection(table)
    mongo.drop_database(db)
