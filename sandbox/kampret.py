# from flask import Flask, flash, redirect, request

from __future__ import division
import re
import request
import requests
import warnings
from bs4 import BeautifulSoup
import htmlmin
import html
import json

from flask import Flask,jsonify,redirect
app = Flask(__name__)

from sandbox import news_scraper,news_crawler

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/scrap/url", methods=['POST'])
def lol():
    result = news_scraper.getnewsKompas(url='https://ekonomi.kompas.com/read/2018/11/28/204200326/cerita-boediono-soal-kesalahan-resep-imf-menangani-krisis-1998')

    jsonresult = {
        'news':result
    }

    end = json.dumps(jsonresult)
    return (end)

@app.route("/crawl", methods=['POST'])
def lmao(source_name,url,target_url):
    result = news_crawler.crawl(source_name,url,target_url)
    return (result)

@app.route("/test",methods=['POST'])
def getnewsKompas(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    prety = soup.prettify()
    divnews = soup.find_all("div",{"class":"read__content"})

    news = ''
    for lol in divnews:
        news = news+lol.get_text()
    return (news)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
