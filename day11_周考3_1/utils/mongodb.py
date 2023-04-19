import pymongo
class Mongodb:
    client=pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )
    db=client['week3']
    table=db['week']