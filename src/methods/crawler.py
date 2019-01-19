# Author: Fuad Ikhlasul Amal, Archie Isdiningrat
# Created date: 07-11-2018
# Updated date: 19-01-2019
# Version: 1.3

from __future__ import division
import os, src.utils.mongodb as mongo
from src.utils.constant import *
from time import strftime
from src.utils.news import News


def crawl(source_alias, url, target_url):
    now = strftime("%Y-%m-%d %H:%M:%S")
    news_source = News(source_alias, url, target_url)

    links = news_source.getArticles()
    raw = news_source.getDomObject()

    instance_ = mongo.getInstance()
    db_ = instance_["milo-" + str(os.getenv('APP_ENV'))]
    LinkCollection = db_.links
    RawCollection = db_.raws

    if raw != {}:
        # build a dom data structure
        data_ = {
            "source": source_alias,
            "url": target_url,
            "content": raw,
            "status": RAW_STATUS['NEW'],
            "created_at": now,
            "updated_at": now
        }

        # do upsert job to dom element collection
        RawCollection.update({"url": target_url}, data_, upsert=True)
        print("insert raw success !!")

    # initialize bulk Op
    LinkBulOp = LinkCollection.initialize_ordered_bulk_op()

    new = 0
    for link in links:
        url_ = {"url": link}
        LinkBulOp.find(url_).upsert().update({
            "$setOnInsert": {"source": source_alias, "status": LINK_STATUS['NEW'], "created_at": now, "updated_at": now},
            "$set": url_
        })

    try:
        LinkBulOp.execute()
        print("insert bulk links success !!")
        return new
    except Exception as e:
        return e
    finally:
        instance_.close()
