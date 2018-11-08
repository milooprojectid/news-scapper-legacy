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
import requests
import warnings
from bs4 import BeautifulSoup



# define GLOBAL STATIC VARIABLE
NEWS_SOURCE_URL = "https://www.detik.com"
NEWS_DOMAIN_URL = "detik.com"
VALID_LINK_URL_RE = re.compile(r"^https?://\S+\." + NEWS_DOMAIN_URL + "/?\S*$")



if __name__ == '__main__':
	warnings.filterwarnings("ignore")

	
	req_ = requests.get(NEWS_SOURCE_URL)
	html_ = req_.text
	soup_ = BeautifulSoup(html_, "html.parser")
	valid_url_counter = 0


	for alink in soup_.findAll("a", href=True):
		href_ = str(alink["href"])
		if VALID_LINK_URL_RE.match(href_):
			print(href_)
