from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hhparser import HHSpider
from jobparser.spiders.sjparser import SJSpider

if __name__=='__main__':
    keys = input("Input key words: ").replace('+', '%2B')
    hh_key, sj_key = keys.replace(' ', '+'), keys.replace(' ', '%20')
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HHSpider, hh_key)
    process.crawl(SJSpider, sj_key)
    print('Waiting... It will take time.')
    process.start()
