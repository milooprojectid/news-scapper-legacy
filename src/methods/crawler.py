# Author: Fuad Ikhlasul Amal
# Created date: 07-11-2018
# Updated date: 26-12-2018
# Version: 1.3
# Function:
#	* perform simple grab html content from http/https web page
# 	* find any url that refer to the self root domain url
#	* collect the urls and grab the HTML page DOMs, save to mongodb
#	* add Flask wrapper and provide API end-point
#	* add hard-coded regexp to classify valid-news-url and non-valid-news-url
#	* add extract and preprocess HTML DOM elements including:
#	*		- remove <script>, <style> and <link> tags
#	* 		- remove inline style="" attribute from any html tag
# 	*		- remove html comments
# 	*		- minified DOM HTML
# Run code: python news_crawler.py
# curl POST -X https://api_host_name_or_ip:api_port_number/crawl {"source": "...", "url": "...", "url_target": "..."}

from __future__ import division
from bs4 import BeautifulSoup, Comment
import re, string, htmlmin, requests
import src.utils.mongodb as mongo


def do_crawl(source_name, url, target_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    req_ = requests.get(target_url, headers=headers)
    html_ = req_.text
    soup_ = BeautifulSoup(html_, "html.parser")
    valid_url_re = re.compile(r"^https?://\S*" + url + "/?\S*$")

    db_ = mongo.getInstance()
    link_collection = db_.links
    dom_collection = db_.raws

    for tag in soup_.findAll():
        if tag.name.lower() in ("script", "style", "link"):
            tag.extract()
        del tag["style"]

    for comment in soup_.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    html_dom_clean = "".join(filter(lambda _: _ in set(string.printable), str(soup_)))
    html_dom_clean = htmlmin.minify(html_dom_clean, remove_comments=True, remove_empty_space=True, remove_all_empty_space=True)

    target_url = target_url.split("?")[0]

    if "detik" == source_name:
        news_url_re = re.compile(r"^(https?://(www\.)?(\S+\.)?detik\.com/[a-z\-]+/\w*\-\d+/[a-z0-9\-]+)$")
    elif "kompas" == source_name:
        pass
    elif "kumparan" == source_name:
        news_url_re = re.compile(r"^(https?://(www\.)?(\S+\.)?kumparan\.com/@?[a-z\-]+/\w*\-\d+/[a-z0-9\-]+\d{19})$")
    else:
        pass

    if news_url_re:
        if news_url_re.match(target_url):
            data_ = {
                "source": source_name,
                "url": target_url,
                "content": html_dom_clean,
                "status": 0,
                "visited_at": None
            }
            dom_collection.update({"content": html_dom_clean, "source": source_name}, data_, upsert=True)
            print("insert dom success !!")

    link_bulk = link_collection.initialize_ordered_bulk_op()

    for alink in soup_.findAll("a", href=True):
        href_ = str(alink["href"]).strip().lower()
        href_ = href_.split("?")[0]

        if valid_url_re.match(href_):
            url_ = {"url": href_, "source": source_name}
            link_bulk.find(url_).upsert().update({
                "$setOnInsert": {"status": 0, "visited_at": None},
                "$set": url_
            })

    try:
        bulkop_resp = link_bulk.execute()
        print("insert bulk links success !!")
        return True
    except Exception as e:
        return None
