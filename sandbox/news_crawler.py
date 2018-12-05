# !/usr/bin/env python
# -*-coding: utf-8 -*-
# system module



# Author: Fuad Ikhlasul Amal
# Created date: 07-11-2018
# Updated date: 05-12-2018
# Version: 1.2
# Function: 
#	* perform simple grab html content from http/https web page
# 	* find any url that refer to the self root domain url
#	* collect the urls and grab the HTML page DOMs, save to mongodb
#	* add Flask wrapper and provide API end-point
#	* add regexp to classify valid-news-url and non-valid-news-url
#	* add extract and preprocess HTML DOM elements including: 
#	*		- remove <script>, <style> and <link> tags
#	* 		- remove inline style="" attribute from any html tag
# 	*		- remove html comments
# 	*		- minified DOM HTML
# Run code: python news_crawler.py
# curl POST -X https://api_host_name_or_ip:api_port_number/crawl {"source": "...", "url": "...", "url_target": "..."}



from __future__ import division
import re
import os
import sys
import string
import htmlmin
import pymongo
import requests
import warnings
from bs4 import BeautifulSoup, Comment
from flask import Flask, request as flask_req, jsonify



warnings.filterwarnings("ignore")
app = Flask(__name__)

_BASEDIR = os.path.dirname(os.path.realpath(__file__))



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
	dom_collection = db_.raws


	# remove <script>, <style> and <link>
	soup_raw = soup_
	for tag in soup_.findAll():
		if tag.name.lower() in ("script", "style", "link"):
			tag.extract()
		# remove inline style in every html tag
		del tag["style"]


	# remove comments block
	for comment in soup_.findAll(text=lambda text:isinstance(text, Comment)):
		comment.extract()


	# handle some non-ascii chars issue
	html_dom_clean = filter(lambda _: _ in set(string.printable), str(soup_))


	# minified dom
	html_dom_clean = htmlmin.minify(html_dom_clean)


	# save the dom page here, but before that, we've to make sure that the link caontains the actual article or news
	# to detect the valid url, using regexp but may vary for each news sources.
	# first, I hard-coded it:
	target_url = target_url.split("?")[0]
	if "detik" == source_name:
		news_url_re = re.compile(r"^(https://(www\.)?(\S+\.)?detik\.com/[a-z\-]+/\w\-\d+/[a-z0-9\-]+)$")
	elif "kompas" == source_name:
		pass
	elif "kumparan" == source_name:
		pass
	else:
		pass


	if news_url_re.match(target_url):
		pass
		# dom_collection.upsert()


	# =================== this block line of code is temporary, to be deleted ===================
	# html_ = filter(lambda _: _ in set(string.printable), html_)
	# fhtml_raw = open(os.path.join(_BASEDIR, "html_dom_raw_sample.out"), "w")
	# sys.stdout = fhtml_raw
	# print(html_)
	# sys.stdout = sys.__stdout__
	# fhtml_raw.close()

	# fhtml_clean = open(os.path.join(_BASEDIR, "html_dom_clean_sample.out"), "w")
	# sys.stdout = fhtml_clean
	# print(htmlmin.minify(html_dom_clean))
	# sys.stdout = sys.__stdout__
	# fhtml_clean.close()
	# =================== this block line of code is temporary, to be deleted ===================


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
		return True
	except Exception, e:
		return None



# Flask methods below:
@app.route("/crawl", methods=["POST"])
def crawl():
	source_name = flask_req.form.get("source")
	url = flask_req.form.get("url")
	url_target = flask_req.form.get("url_target")

	if do_crawl(source_name, url, url_target):
		return jsonify({"response": "ok"})
	else:
		return jsonify({"response": "not-ok"})



if __name__ == '__main__':
	# this is the actual way to call crawl service
	# app.run(debug=True)

	# code below was provided for testing purpose
	do_crawl("detik", "detik.com", "https://finance.detik.com/berita-ekonomi-bisnis/d-4332042/anggaran-beasiswa-lpdp-naik-jadi-rp-55-triliun?tag_from=wp_nhl_judul_8&_ga=2.30128319.1057623162.1544025778-523514988.1519287610")
