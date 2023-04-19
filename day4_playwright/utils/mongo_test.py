import pymongo


if __name__ == '__main__':
    client = pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )

    # 创建数据库mysql
    # create database dbname if not exists
    db=client.client['2010A_3_24']

    # 创建表
    # create table tablename if not exists(字段名：约束)
    table=db['2010A_3_24']

    # 数据库添加数据
    """
    添加一条数据
    """
    info={'name':'刘奇梦','tel':'18720464463'}
    table.insert_one(info)

    """
    添加多条数据
    """
    infos=[
        {'姓名':'刘奇梦1','tel':'18720464463'},
        {'姓名': '刘奇梦2', 'tel': '18720464464'},
        {'姓名': '刘奇梦3', 'tel': '18720464465'}
    ]
    table.insert_many(infos)

    # 简单查询
    for i in table.find():
        print(i)