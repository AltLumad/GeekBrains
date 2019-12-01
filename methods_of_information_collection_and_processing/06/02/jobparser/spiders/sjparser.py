# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

class SJSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']
    _url_sj = 'https://www.superjob.ru'
    def __init__(self, key):
        SJSpider.start_urls = ['https://www.superjob.ru/vacancy/search/?keywords={}&geo%5Bc%5D%5B0%5D=1'.format(key)]

    def parse(self, response: HtmlResponse):
        try:
            next_page = SJSpider._url_sj + response.xpath('//a[contains(@rel,"next")]/@href').extract_first()
            yield response.follow(next_page, callback=self.parse)
        except:
            pass


        vacansy_items =  response.xpath('//div//a[contains(@href,"vakansii")]/@href').extract()
        for link in vacansy_items:
            yield response.follow(SJSpider._url_sj + link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_value('source', 'SJ')
        loader.add_xpath('name', '//h1[contains(@class,"_3mfro")]/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('salary', '//div[contains(@class,"_1Tjoc")]//span[contains(@class,"_3mfro _2Wp8I ")]/span/text()')
        yield loader.load_item()





