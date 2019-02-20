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
warnings.filterwarnings("ignore")

#using nespaper library
def article(dom):
    article = Article('', language ='id', memoize_articles=False)
    article.set_html(dom)
    article.parse()

    return {
        'authors': article.authors,
        'title': article.title,
        'publish_date': article.publish_date,
        'text': article.text
    }

def isEligible(text):
    if not text:
        return False

    splitted = text.split('.')
    if len(splitted) < 3:
        return False

    return True

def migrate():
    instance_ = mongo.getInstance()
    db_ = instance_["milo-" + str(os.getenv('APP_ENV'))]
    doc_collection = db_.docs
    raw_collection = db_.raws
    count = raw_collection.count_documents({"status": RAW_STATUS["NEW"]})
    DocBulkOp = doc_collection.initialize_ordered_bulk_op()
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    for i in tqdm(range(0, count,10),postfix=None, disable=False):
        data = raw_collection.find({"status": RAW_STATUS["NEW"]}).skip(i).limit(10)

        if not DocBulkOp:
            DocBulkOp = doc_collection.initialize_ordered_bulk_op()

        for doc in data:
            content = doc['content']
            try:
                data_to_insert = article(content)

                if isEligible(data_to_insert['text']):
                    DocBulkOp.find({"url": doc["url"]}).upsert() \
                        .update({
                            "$setOnInsert": {
                                "status": RAW_STATUS["NEW"],
                                "created_at": now,
                                "updated_at": now
                            },
                            "$set": {
                                "url": doc["url"],
                                "source": doc["source"],
                                "content": data_to_insert
                            }
                        })
                    raw_collection.update({"url": doc["url"]}, { "$set": {'status': RAW_STATUS['MIGRATED']} })
                else:
                    raw_collection.update({"url": doc["url"]}, { "$set": {'status': RAW_STATUS['INVALID']} })
            except:
               pass

        try:
            DocBulkOp.execute()
        except Exception as err:
            print(err)
        finally:
            DocBulkOp = None

    instance_.close()
    return True


if __name__ == '__main__':
    migrate()
