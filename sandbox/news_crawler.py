# !/usr/bin/env python
# -*-coding: utf-8 -*-
# system module



# Author: Fuad Ikhlasul Amal
# Created date: 07-11-2018
# Updated date: -
# Version: 1.0
# Function: perform simple grab html content from http/https web page
# Run code: python news_crawler.py



from __future__ import division
import re
import pymongo
import requests
import warnings
from bs4 import BeautifulSoup



warnings.filterwarnings("ignore")



def connect_mongodb():
	return pymongo.MongoClient("mongodb://sakoju:E107112358@178.128.98.252:2017/milo-staging?authSource=admin")



def crawl(source_name, url, target_url):
	req_ = requests.get(target_url)
	html_ = req_.text
	soup_ = BeautifulSoup(html_, "html.parser")
	valid_url_re = re.compile(r"^https?://\S*" + url + "/?\S*$")
	

	# specify the mongodb connection, database and collection
	db_cnx = connect_mongodb()
	db_ = db_cnx["milo-staging"]
	link_collection = db_.links


	for alink in soup_.findAll("a", href=True):
		href_ = str(alink["href"]).strip().lower()
		if valid_url_re.match(href_):
			link_collection.insert_one({
				"url": href_, "source": source_name,
				"status": 
			})
			# save link here, one-by-one inside loop


	# bulk save here, list of links...



if __name__ == '__main__':
	crawl("detik", "detik.com", "https://www.detik.com")