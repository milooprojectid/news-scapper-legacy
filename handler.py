from src.methods.crawler import do_crawl as crawl
from src.utils.helpers import response

def crawler_handler(event, context):
    # TODO: validate input
    # TODO: map input to function dynamically

    crawl("detik", "detik.com", "https://hot.detik.com/kpop/d-4340712/heboh-iklan-blackpink-dinilai-seronok-shopee-dipanggil-kpai")
    return response('crawl completed')


