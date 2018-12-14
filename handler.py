# from src.methods.crawler import do_crawl as crawl
from src.utils.helpers import response


def crawler_handler(event, context):
    return response('crawl complete')
