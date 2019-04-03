from src.methods.crawler import crawl
from os.path import join, dirname
from dotenv import load_dotenv

# load env
load_dotenv(join(dirname(__file__), '.env'))

# local tester
if __name__ == '__main__':
    source = 'detik'
    link = 'detik.com'
    target = 'https://news.detik.com/berita/d-4438905/pelajar-ri-kerjai-layanan-as-kpai-ingatkan-konten-negatif-film'
    crawl(source, link, target)