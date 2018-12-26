from src.methods.crawler import do_crawl as crawl
from src.utils.helpers import response
from os.path import join, dirname
from dotenv import load_dotenv

# load env
load_dotenv(join(dirname(__file__), '.env'))

def crawler_handler(event, context):
    # TODO: validate input
    # TODO: map input to function dynamically

    crawl("detik", "detik.com", "https://detik.com")
    return response('crawl completed')