from src.methods.crawler import do_crawl as crawl
from os.path import join, dirname
from dotenv import load_dotenv

# load env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# local tester
if __name__ == '__main__':
    source = input('source name : ')
    link = input('source url  : ')
    target = input('targer url  : ')
    crawl(source, link, target)
