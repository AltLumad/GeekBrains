# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

import re


class HHSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = []

    def __init__(self, key):
        HHSpider.start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text={}&showClusters=true'.format(key)]

    def parse(self, response: HtmlResponse):
        try:
            next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
            yield response.follow(next_page, callback=self.parse)
        except:
            pass
        vacansy_items = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacansy_items:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_value('source', 'HH')
        loader.add_xpath('name', '//div[contains(@class,"vacancy-title")]//h1//text()')
        loader.add_value('link', response.url)
        loader.add_xpath('salary', '//span[contains(@itemprop,"baseSalary")]//@content')
        yield loader.load_item()





