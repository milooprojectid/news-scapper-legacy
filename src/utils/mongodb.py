import pymongo, os

def getInstance():
    return pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
