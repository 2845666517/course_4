import pymongo
class Pymongo():
    mongo=pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )
    db=mongo['2010A_w2_1']
    table=db['2010A_w2_1']
    table2=db['2010A_w2_2']