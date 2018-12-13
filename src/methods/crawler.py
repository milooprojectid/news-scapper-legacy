# Author: Fuad Ikhlasul Amal
# Created date: 07-11-2018
# Updated date: 28-11-2018
# Version: 1.2
# Function: 
#	* perform simple grab html content from http/https web page
# 	* find any url that refer to the self root domain url
#	* collect the urls and save to database
#	* add Flask wrapper
#	* add extract, pre-process and save DOM elements function
# Run code: python crawler.py

from __future__ import division
from bs4 import BeautifulSoup, Comment
import src.utils.mongodb as mongo
import re, sys, requests, warnings

warnings.filterwarnings("ignore")

def do_crawl(source_name, url, target_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    req_ = requests.get(target_url, headers=headers)
    html_ = str(req_.text)
    soup_ = BeautifulSoup(html_, "html.parser")
    valid_url_re = re.compile(r"^https?://\S*" + url + "/?\S*$")

    # specify the mongodb connection, database and collection
    db_ = mongo.getInstance()
    link_collection = db_.links

    # remove <script>, <style> and <link>
    soup_raw = soup_
    for tag in soup_.findAll():
        if tag.name.lower() in ("script", "style", "link"):
            tag.extract()
    # remove inline style in html tag
    # for attr

    # remove comments block
    for comment in soup_.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    fhtml_raw = open("html_dom_raw_sample.out", "w")
    sys.stdout = fhtml_raw
    print(html_)
    sys.stdout = sys.__stdout__
    fhtml_raw.close()

    fhtml_clean = open("html_dom_clean_sample.out", "w")
    sys.stdout = fhtml_clean
    print(soup_)
    sys.stdout = sys.__stdout__
    fhtml_clean.close()

    # quit()

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
        return True
    except Exception:
        return None


if __name__ == '__main__':
    # app.run(debug=True)
    do_crawl("viva", "viva.co.id", "https://www.viva.co.id/")
