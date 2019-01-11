from dotenv import load_dotenv
from os.path import join, dirname
from tqdm import tqdm
import os, time
load_dotenv(join(dirname(__file__), '../../.env'))

import src.utils.mongodb as mongo

if __name__ == '__main__':
    instance_ = mongo.getInstance()
    db_ = instance_["milo-" + os.getenv('APP_ENV')]
    raw_collection = db_.raws
    count = raw_collection.count_documents({})

    for i in tqdm(range(0, count, 10), postfix=None):
        data = raw_collection.find().skip(i).limit(10)
        # for doc in data:
        #     print(doc['content'])
        #     normalize doc
        #     update doc
        # time.sleep(0.5)

