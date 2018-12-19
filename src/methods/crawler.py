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
from bs4 import BeautifulSoup, Comment
import re, string, htmlmin, requests
import src.utils.mongodb as mongo
from src.utils.regex import news_regex as regex

def do_crawl(source_alias, url, target_url):
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

    # check regex
    if source_alias in regex.keys():
        news_url_re = re.compile(regex[source_alias])
        if news_url_re.match(target_url):
            data_ = {
                "source": source_alias,
                "url": target_url,
                "content": html_dom_clean,
                "status": 0,
                "visited_at": None
            }
            dom_collection.update({"content": html_dom_clean, "source": source_alias}, data_, upsert=True)
            print("insert dom success !!")

    link_bulk = link_collection.initialize_ordered_bulk_op()

    for alink in soup_.findAll("a", href=True):
        href_ = str(alink["href"]).strip().lower()
        href_ = href_.split("?")[0]

        if valid_url_re.match(href_):
            url_ = {"url": href_, "source": source_alias}
            link_bulk.find(url_).upsert().update({
                "$setOnInsert": {"status": 0, "visited_at": None},
                "$set": url_
            })

    try:
        link_bulk.execute()
        print("insert bulk links success !!")
        return True
    except Exception as e:
        return None
