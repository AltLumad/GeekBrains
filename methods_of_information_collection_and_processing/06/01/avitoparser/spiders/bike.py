# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader

class AvitoBikeSpider(scrapy.Spider):
    name = 'bike'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/velosipedy']
    npage = 2

    def parse(self, response: HtmlResponse):
        try:
            next_page = 'https://www.avito.ru/moskva/velosipedy' + response.xpath(f'//a[contains(text(), "{AvitoBikeSpider.npage}")]/@href').extract_first()
            AvitoBikeSpider.npage += 1
            yield response.follow(next_page, callback=self.parse)
        except:
            pass
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        loader.add_value('link', response.url)
        loader.add_xpath('photos', '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_xpath('price', '//span[@class="js-item-price"]/text()')
        loader.add_xpath('currency', '//span[@itemprop="priceCurrency"]/@content')
        loader.add_xpath('address', '//div[@class="item-address"]')
        loader.add_xpath('description', '//div[@class="item-description"]//text()')
        yield loader.load_item()

