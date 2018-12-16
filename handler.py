from src.methods.crawler import do_crawl as crawl
from src.utils.helpers import response
from os.path import join, dirname
from dotenv import load_dotenv

# load env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def crawler_handler(event, context):
    # TODO: validate input
    # TODO: map input to function dynamically

    crawl("detik", "detik.com", "https://hot.detik.com/kpop/d-4340712/heboh-iklan-blackpink-dinilai-seronok-shopee-dipanggil-kpai")
    return response('crawl completed')


