# !/usr/bin/env python
# -*-coding: utf-8 -*-
# system module

from __future__ import division
import warnings
from newspaper import Article
from dotenv import load_dotenv
from os.path import join, dirname
from tqdm import tqdm
import os, time
from src.utils.constant import *
load_dotenv(join(dirname(__file__),'../../.env'))

import src.utils.mongodb as mongo
import src.utils.news as News

warnings.filterwarnings("ignore")


#using nespaper library
def article(dom):
    article = Article('', language ='id', memoize_articles=False)
    # article.download()
    article.html = dom
    article.parse()

    title = article.title
    author = article.authors
    news = article.text
    date = article.publish_date
    # link = article.link_hash

    data = {
        "title": title,
        "date": date,
        "content": news,
        "author": author
    }
    return(data)

def scrap():

    instance_ = mongo.getInstance()
    db_ = instance_["milo-" + str(os.getenv('APP_ENV'))]
    doc_collection = db_.doc
    raw_collection = db_.raws
    count = raw_collection.count_documents({})
    DocBulkOp = doc_collection.initialize_ordered_bulk_op()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    doc_count = 0

    for i in tqdm(range(420,count,10),postfix=None, disable=False):
        data = raw_collection.find().skip(i).limit(10)

        # create bucket list for raw document and initialize py-mongodb bulk object
        # corp = []
        print("for")
        if not DocBulkOp:
            DocBulkOp = doc_collection.initialize_ordered_bulk_op()

        for doc in data:
            content = doc['content']
            # print(doc['url'])
            try:
                print("try")
                data_to_insert = article(content)
                data_to_insert.update({
                    "url": doc["url"],
                    "source": doc["source"]
                })
                # corp.append(article(content))
                DocBulkOp.find({"url": doc["url"]}).upsert() \
                    .update({
                        "$setOnInsert": {
                            "status": DOC_STATUS["NEW"],
                            "created_at": now,
                            "updated_at": now
                        },
                        "$set": data_to_insert
                    })
                doc_count += 1
            except:
                print('whoops')

        try:
            # save 10 record at once
            DocBulkOp.execute()
            DocBulkOp = None
        except Exception as e:
            return e

    instance_.close()
    return doc_count


if __name__ == '__main__':
   print(scrap())