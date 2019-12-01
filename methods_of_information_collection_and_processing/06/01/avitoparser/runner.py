from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser.spiders.bike import AvitoBikeSpider
from avitoparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoBikeSpider)
    process.start()

