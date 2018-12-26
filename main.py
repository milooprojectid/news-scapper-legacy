from src.methods.crawler import do_crawl as crawl
from os.path import join, dirname
from dotenv import load_dotenv
from src.utils.pusher import publish

# load env
load_dotenv(join(dirname(__file__), '.env'))

# local tester
if __name__ == '__main__':
    # source = raw_input('source name : ')
    # link = raw_input('source url  : ')
    # target = raw_input('targer url  : ')
    source = 'detik'
    link = 'detik.com'
    target = 'https://news.detik.com/berita/d-4352982/tgb-jadi-rebutan'
    crawl(source, link, target)
    publish()