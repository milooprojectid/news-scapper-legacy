# !/usr/bin/env python
# -*-coding: utf-8 -*-
# system module



# Author: Fuad Ikhlasul Amal
# Created date: 07-11-2018
# Updated date: 28-11-2018
# Version: 1.2
# Function: 
#	* perform simple grab html content from http/https web page
# 	* find any url that refer to the self root domain url
#	* collect the urls and save to database
#	* add Flask wrapper
# Run code: python news_crawler.py



from __future__ import division
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



def do_crawl(source_name, url, target_url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
	req_ = requests.get(target_url, headers=headers)
	html_ = req_.text
	soup_ = BeautifulSoup(html_, "html.parser")
	valid_url_re = re.compile(r"^https?://\S*" + url + "/?\S*$")
	

	# specify the mongodb connection, database and collection
	db_cnx = connect_mongodb()
	db_ = db_cnx["milo-staging"]
	link_collection = db_.links


	# init the mongo bulk object to upsert (update-or-insert) the link data
	link_bulk = link_collection.initialize_ordered_bulk_op()


	for alink in soup_.findAll("a", href=True):
		href_ = str(alink["href"]).strip().lower()
		
		# remove params or arguments from url after '?'
		href_ = href_.split("?")[0]

		if valid_url_re.match(href_):
			url_ = {"url": href_, "source": source_name}
			# save link here, one-by-one inside loop
			link_bulk.find(url_).upsert().update({
				"$setOnInsert": {"status": 0, "visited_at": None},
				"$set": url_
			})


	# bulk save here, list of links...
	try:
		bulkop_resp = link_bulk.execute()
		return "ok"
	except Exception as e:
		return None



# Flask methods below:
@app.route("/crawl", methods=["POST"])
def crawl():
	source_name = flask_req.form.get("source_name")
	url = flask_req.form.get("url")
	url_target = flask_req.form.get("url_target")

	if do_crawl(source_name, url, url_target):

		return jsonify({"response": "ok"})
	else:
		return jsonify({"response": "not ok"})



if __name__ == '__main__':
	app.run(debug=True)
