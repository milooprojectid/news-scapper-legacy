import pymongo, os

def getInstance():
    connection =  pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
    return connection["milo-staging"]
