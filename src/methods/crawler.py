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
from src.utils.regex import news_regex
from src.utils.constant import *
from time import strftime



def do_crawl(source_alias, url, target_url):
    now = strftime("%Y-%m-%d %H:%M:%S")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    req_ = requests.get(target_url, headers=headers)
    html_ = req_.text
    soup_ = BeautifulSoup(html_, "html.parser")
    # to make s
    valid_url_re = re.compile(r"^https?://\S*" + url + "/?\S*$")

    db_ = mongo.getInstance()
    link_collection = db_.links
    dom_collection = db_.raws

    for tag in soup_.findAll():
        # remove all <script>, <style> and <link> tags
        if tag.name.lower() in ("script", "style", "link"):
            tag.extract()
        # remove all tag inline style attributes
        del tag["style"]

    # remove all those non-sense comments as this comment is
    for comment in soup_.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # prep and cleansing the dom element before it's being stored on db
    html_dom_clean = "".join(filter(lambda _: _ in set(string.printable), str(soup_)))
    html_dom_clean = htmlmin.minify(html_dom_clean, remove_comments=True, remove_empty_space=True, remove_all_empty_space=True)
    # split the question mark to split query parameter from the url string
    target_url = target_url.split("?")[0]

    if source_alias in news_regex.keys():
        news_url_re = re.compile(news_regex[source_alias])
        # check if the target_url match the valid contained-article url regexp pattern
        if news_url_re.match(target_url):
            # build a dom data structure
            data_ = {
                "source": source_alias,
                "url": target_url,
                "content": html_dom_clean,
                "status": RAW_STATUS['NEW'],
                "created_at": now,
                "updated_at": now
            }
            # do upsert job to dom element collection
            dom_collection.update({"content": html_dom_clean, "source": source_alias}, data_, upsert=True)
            print("insert dom success !!")

    # initialize pymongo bulk upserter object to prevent inside a loop once-in-a-time upsert, insted, one-time bulk upsert
    link_bulk = link_collection.initialize_ordered_bulk_op()

    new = 0
    for alink in soup_.findAll("a", href=True):
        # extract the value of href attribut from <a> tag
        href_ = str(alink["href"]).strip().lower()
        # split the question mark to split query parameter from the url string
        href_ = href_.split("?")[0]

        if valid_url_re.match(href_):
            new += 1
            url_ = {"url": href_, "source": source_alias}
            # create exact current time in a desired format

            # append upsert list element into pymongo bulk upserter object 
            link_bulk.find(url_).upsert().update({
                "$setOnInsert": {"status": LINK_STATUS['NEW'], "created_at": now, "updated_at": now},
                "$set": url_
            })
    try:
        # actual mongodb upsert process here
        link_bulk.execute()
        print("insert bulk links success !!")
        return new
    except Exception as e:
        return e
