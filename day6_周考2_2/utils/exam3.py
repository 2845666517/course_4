import pymongo
if __name__ == '__main__':
    # 建立与本地已经运行的mongodb的连接
    mongo=pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )
    # 使用正确的指令创建一个数据库zngc_db
    db=mongo['zngc_db']

    # 使用正确的指令创建数据集合zngc_sites
    table=db['zngc_sites']

    # 使用正确的指令插入以下数据
    # 数据如下：
    student1 = {
        'id': '20170101',
        'name': 'Jordan',
        'age': 20,
        'gender': 'male'
    }
    student2 = {
        'id': '20170202',
        'name': 'Mike',
        'age': 21,
        'gender': 'female'
    }
    table.insert_one(student1)
    table.insert_one(student2)

    # 正确获取集合中gender不等于malea且ge的大于20，的数据
    print(list(table.find({'gender':{'$ne':'malea'},'age':{'$gt':20}})))

    # 可以正常修改age为20的数据，将name修改为迈克
    table.update_many({'age':20}, {'$set': {'name':'迈克'}})
    print(list(table.find()))

    # 根据序号id，数据是如何降序排序的呢（通过聚合函数实现降序功能）
    dom=[
        {'$sort': {'id':-1}}
    ]
    res=table.aggregate(dom)
    for i in res:
        print(i)
    # 使用正确指令删除所有的数据，以及删除数据集合
    table.delete_many({})
    db.drop_collection(table)
    mongo.drop_database(db)
