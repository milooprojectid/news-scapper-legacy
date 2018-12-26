import os
from src.methods.crawler import do_crawl as crawl
from src.utils.helpers import response
from src.transformer.input_transformer import normalize
from os.path import join, dirname
from dotenv import load_dotenv

# load env
load_dotenv(join(dirname(__file__), '.env'))

def crawler_handler(event, context):
    try:
        if event['headers']['secret'] != os.getenv('API_SECRET'):
            return response('not authorized', status=401)

<<<<<<< HEAD
    crawl("detik", "detik.com", "https://detik.com")
    return response('crawl completed')
=======
        # get request input
        [source, url, target_url] = normalize(event)

        # crawl target url
        crawl(source, url, target_url)

        return response('crawl completed', {'new': 0, 'done': 1})
    except:
        return response('an error occurred', status=500)
>>>>>>> 5648cb84a6ea54bbaeb4f30cab98542e29fe12c2
