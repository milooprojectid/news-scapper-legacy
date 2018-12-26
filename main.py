from src.methods.crawler import do_crawl as crawl
from os.path import join, dirname
from dotenv import load_dotenv
from src.utils.pusher import publish

# load env
load_dotenv(join(dirname(__file__), '.env'))

# local tester
if __name__ == '__main__':
    # source = input('source name : ')
    # link = input('source url  : ')
    # target = input('targer url  : ')
    # crawl(source, link, target)
    publish()