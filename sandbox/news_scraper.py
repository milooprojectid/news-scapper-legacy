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
from flask import Flask, request as flask_req,jsonify


warnings.filterwarnings("ignore")
app = Flask(__name__)


def connect_mongodb():
	return pymongo.MongoClient("mongodb://sakoju:E107112358@178.128.98.252:2017/milo-staging?authSource=admin")

def get_dom():
    mydb = connect_mongodb()
    dom = mydb[]
    return (dom)

def getNewsKompasN():
    dom = get_dom()
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
    news = ''
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


def cleanDOM(dom):
    clean = htmlmin.minify(dom)
    return(clean)


a = getnewsKompas('https://nasional.kompas.com/read/2018/12/05/16252441/dengan-suara-meninggi-prabowo-cibir-media-massa-soal-jumlah-peserta-reuni')
#
print(a)
# print(getnewsKompas(a))

# Flask methods below:
@app.route("/scrap", methods=["POST"])
def scrap():
    dom = flask_req.form.get("dom")
	# source_name = flask_req.form.get("source_name")
	# url = flask_req.form.get("url")
	# url_target = flask_req.form.get("url_target")
    source =''
    if (source == 'Kumparan'):
        scr = getNewsKumparan(dom)
    if (source == 'Kompas'):
        scr = getnewsKompas(dom)
    if (source == 'OKEZone'):
        scr = getNewsOKEZone(dom)

    return jsonify(scr)

if __name__ == '__main__':
	app.run(debug=True)

