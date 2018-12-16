import pymongo

def getInstance():
    connection =  pymongo.MongoClient("mongodb://sakoju:E107112358@178.128.98.252:2017/milo-staging?authSource=admin")
    return connection["milo-staging"]
