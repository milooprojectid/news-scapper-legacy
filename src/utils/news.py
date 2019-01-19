from newspaper import Article, build
from src.utils.regex import news_regex
import re

class News:
    __Articles = []
    __ValidUrlRegex = None
    __Alias = ""
    __Url = ""
    __TargetUrl = ""
    __DomStatus = False
    __DomObject = {}

    def __init__(self, alias, url, target_url):
        self.__Alias = alias
        self.__Url = url
        self.__TargerUrl = target_url
        self.__ValidUrlRegex = re.compile(r"^https?://\S*" + url + "/?\S*$")

        self.__determineDomStatus()
        self.__generateArticles()

        if self.__DomStatus:
            self.__generateCleansedDom()


    def __determineDomStatus(self):
        if self.__Alias in news_regex.keys():
            news_url_re = re.compile(news_regex[self.__Alias])
            self.__DomStatus = news_url_re.match(self.__TargerUrl)

    def __generateArticles(self):
        source = build(self.__TargerUrl, language='id', memoize_articles=False)
        containers = []
        for article in source.articles:
            _href = article.url.split('?')[0]
            if not _href in containers and self.__ValidUrlRegex.match(_href):
                containers.append(_href)
        self.__Articles = containers

    def __generateCleansedDom(self):
        news = Article(self.__TargerUrl, language='id')
        news.download()
        news.parse()
        self.__DomObject = {
            'authors': news.authors,
            'title': news.title,
            'publish_date': news.publish_date,
            'text': news.text
        }

    def getArticles(self):
        return self.__Articles

    def getDomObject(self):
        return self.__DomObject