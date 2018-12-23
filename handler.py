import os
from src.methods.crawler import do_crawl as crawl
from src.utils.helpers import response
from src.utils.pusher import publish
from src.transformer.input_transformer import normalize
from os.path import join, dirname
from dotenv import load_dotenv

# load env
load_dotenv(join(dirname(__file__), '.env'))

def crawler_handler(event, context):
    try:
        if event['headers']['secret'] != os.getenv('API_SECRET'):
            return response('not authorized', status=401)

        # get request input
        [source, url, target_url] = normalize(event)

        # crawl target url
        nLinks = crawl(source, url, target_url)

        # publish event
        publish('home', 'link-changed', {'all': nLinks, 'done': 1})

        return response('crawl completed')
    except:
        return response('an error occurred', status=500)
