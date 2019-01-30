# !/usr/bin/env python
# -*-coding: utf-8 -*-
# system module

from __future__ import division
import re
import requests
import warnings
from bs4 import BeautifulSoup
import htmlmin
import html

import re
import sys
import pymongo
import requests
import warnings
from bs4 import BeautifulSoup
# from flask import Flask, request as flask_req,jsonify


from newspaper import Article



warnings.filterwarnings("ignore")
# app = Flask(__name__)


def connect_mongodb():
	return pymongo.MongoClient("mongodb://sakoju:E107112358@178.128.98.252:2017/milo-staging?authSource=admin")

def get_dom():
    mydb = connect_mongodb()
    # dom = mydb["milo-staging"].raws.find_one(sort=[('id',pymongo.DESCENDING)])
    # print("=========",dom)
    content = mydb['milo-staging'].raws.find_one({},{'content':1, '_id': 0})
    source = mydb['milo-staging'].raws.find_one({},{'source':1,'_id':0})
    url = mydb['milo-staging'].raws.find_one({},{'url':1,'_id':0})
    # print('source = ',source)
    # print('this is lol : \n',content)
    return (source,url,content)


def getNews():
    #cek dom source
    source, url, content = get_dom()
    source = getSourceOnly(source)
    if source == "'detik'":
        content = getContentOnly(content)
        # print("=======",content)
        corpus = getNewsDetik(content)
        result = corpus
    if source == "'kompas'":
        corpus = getNewsKompasN()
        result = corpus
    if source == "'kumparan'":
        corpus = getNewsKumparan()
        result = corpus
    # else:
    #     corpus = 'not sure'
    #     result = corpus
    return (result)


def getNewsKompasN():
    dom = get_dom()
    dom = BeautifulSoup(dom,'html.parser')
    divnews = dom.find_all("div",{"class":"read__content"})
    title = dom.find("h1",{"class":"read__title"}).get_text()
    date = dom.find("div",{"class":"read__time"}).get_text()
    author = dom.find("div",{"class":"read__author"}).get_text()
    news = ''
    for i in divnews:
        news = news + i.get_text()

    result = {
        "Title": title,
        "date": date,
        "author": author,
        "News": news
    }

    return (result)

def getNewsDetik(content):
    # source,url,content = get_dom()
    # newsHTML = content

    dom = BeautifulSoup(content,'html.parser')
    news = dom.find("div",{"class":"itp_bodycontent detail_text"}).get_text()
    date = dom.find("div",{"class":"date"}).get_text()
    title = dom.find("h1").get_text()
    author = dom.find("div",{"class":"author"}).get_text()

    result = {
        "Title": title,
        "date": date,
        "author": author,
        "News": news
    }
    return (result)


def getNewsCNN():
    dom = ''
    dom  = BeautifulSoup(dom,'html.parser')
    news = ''
    date = dom.find('')
    title = dom.find('')
    author = dom.find('')

    result = {
        "Title": title,
        "date": date,
        "author": author,
        "News": news
    }
    return (result)

def getnewsKompas(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    # print(soup)
    prety = soup.prettify()
    divnews = soup.find_all("div",{"class":"read__content"})
    title = soup.find("h1", {"class": "read__title"}).get_text()
    date = soup.find("div", {"class": "read__time"}).get_text()
    author = soup.find("div", {"class": "read__author"}).get_text()
    news = ''
    for lol in divnews:
        news = news+lol.get_text()
    result = {
        "Title": title,
        "date": date,
        "author": author,
        "News": news
    }
    return (result)

def getNewsKumparan(dom):

    divnews = dom.find_all("div",{"class":"editor-padding-8"})
    title = ''
    date = ''
    author = ''
    news = dom.find_all("span",{"data-slate-content":"true"})
    for i in divnews:
        news = news+i.get_text()

    result = {
        "Title": title,
        "date": date,
        "author": author,
        "News": news
    }

    return (result)

def getNewsOKEZone(dom):
    divnews = ''
    title = ''
    date = ''
    author = ''
    news = ''

    result = {
        "Title": title,
        "date": date,
        "author": author,
        "News": news
    }

    return (result)


def getContentOnly(content):

    value = str(content)
    result = re.sub("{'content': ","",value)
    result = re.sub("{|}","",result)
    return (result)

def getSourceOnly(source):
    value = str(source)
    result = re.sub("{'source': ","",value)
    result = re.sub("{|}","",result)
    return (result)



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

    return(title,date, author, news)


def saveToMongo(source, date, author, news):
    # db_ = mongo.getInstance()
    # link_collection = db_.links
    # dom_collection = db_.corpus
    data_ = {
        "source": source,
        "date": date,
        "content": news,
        "author": author
    }
    # do upsert job to dom element collection
    # return dom_collection.update({"source": source,"date": date,"content": news,"author": author }, data_, upsert=True)



from dotenv import load_dotenv
from os.path import join, dirname
from tqdm import tqdm
import os, time
load_dotenv(join(dirname(__file__),'../../.env'))

import src.utils.mongodb as mongo
import src.utils.news as News

if __name__ == '__main__':
    # b,c,d = get_dom()
    # d = getContentOnly(d)
    #
    # print("getnews no lib\n", getNews())
    #
    # print('using lib indo\n',article(d))
    #
    # source = getSourceOnly(b)
    # news = getNews()

    # url = 'https://arabic.cnn.com/middle-east/article/2019/01/02/egypt-sisi-economic-reforms'
    # print('using library \n',article(url))

    instance_ = mongo.getInstance()
    db_ = instance_["milo-" + str(os.getenv('APP_ENV'))]
    raw_collection = db_.raws
    count = raw_collection.count_documents({})

    corp = []
    for i in tqdm(range(420,count,10),postfix=None, disable=True):
        data = raw_collection.find().skip(i).limit(10)
        for doc in data:
            content = doc['content']
            print(doc['url'])
            try:
                corp.append(article(content))
            except:
                print('whoops')
            # print(corp)

    # print(corp)