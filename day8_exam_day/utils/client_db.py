import pymongo
class Mongodb:
    client=pymongo.MongoClient(
        host='127.0.0.1',
        port=3306
    )
    db=client['3_29']
    table=db['3_29']