import pymongo
class Mogodb:
    client=pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )
    db=client['2010A_w2_1']
    talbe=db['2010A_w2_1']