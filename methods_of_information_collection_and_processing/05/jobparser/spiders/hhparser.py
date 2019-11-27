# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
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
        name = response.xpath('//div[contains(@class,"vacancy-title")]//h1//text()').extract_first()
        link = response.url
        currency = min_salary = max_salary = None
        try:
            currency = response.xpath('//span[contains(@itemprop,"baseSalary")]/meta/@content').extract_first()
            tmp = response.xpath('//span[contains(@itemprop,"baseSalary")]/span//@content').extract()
            min_salary = int(''.join(re.split('\s', tmp[0])))
            if (len(tmp)==3) : max_salary = int(''.join(re.split('\s', tmp[1])))
        except:
            pass

        yield JobparserItem(name=name, link=link, currency=currency, min_salary=min_salary, max_salary=max_salary, source="HeadHunter")





