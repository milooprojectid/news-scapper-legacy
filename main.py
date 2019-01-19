from src.methods.crawler import crawl
from os.path import join, dirname
from dotenv import load_dotenv

# load env
load_dotenv(join(dirname(__file__), '.env'))

# local tester
if __name__ == '__main__':
    source = 'detik'
    link = 'detik.com'
    target = 'https://food.detik.com/readfoto/2019/01/09/101521/4376819/484/20-roti-bakar-empuk-enak-ada-di-sini'
    crawl(source, link, target)