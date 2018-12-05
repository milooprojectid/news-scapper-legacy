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


def getNewsKompas(dom):
    divnews = dom.find_all("div",{"class":"read__content"})
    news = ''
    for lol in divnews:
        news = news+lol.get_text()
    return (news)


def getnewsKompas(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    # print(soup)
    prety = soup.prettify()
    divnews = soup.find_all("div",{"class":"read__content"})

    news = ''
    for lol in divnews:
        news = news+lol.get_text()
    return (soup)

    # title = soup.find()

def getNewsKumparan(dom):
    divnews = dom.find_all("div",{"class":"editor-padding-8"})
    news = ''
    for i in divnews:
        news = news+i.get_text()
    return (news)

def cleanDOM(dom):
    clean = htmlmin.minify(dom)
    return(clean)


a = getnewsKompas('https://ekonomi.kompas.com/read/2018/11/28/204200326/cerita-boediono-soal-kesalahan-resep-imf-menangani-krisis-1998')

print(a)
print(getNewsKompas(a))

# Flask methods below:
@app.route("/scrap", methods=["POST"])
def scrap():
    dom = flask_req.form.get("dom")
	# source_name = flask_req.form.get("source_name")
	# url = flask_req.form.get("url")
	# url_target = flask_req.form.get("url_target")
    scr = getNewsKompas(dom)
    title = 0
    date = 0
    author = 0
    result = {
        "Title" :title,
        "date" :date,
        "author": author,
        "News":scr
    }
    return jsonify(result)

	# if getNewsKompas(dom):
	# 	return jsonify({"response": "ok"})
	# else:
	# 	return jsonify({"response": "not ok"})


if __name__ == '__main__':
	app.run(debug=True)
