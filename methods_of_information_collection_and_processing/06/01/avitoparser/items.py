# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def pretty_price(price):
    result = None
    try:
        result = float(''.join(re.split('\s', price)))
    except:
        pass
    return result


def pretty_address(field):
    result = None
    try:
        result = ''.join(re.split('<.*>', field)).strip()
    except:
        pass
    return result

def pretty_description(field):
    result = None
    try:
        result = ''.join(field).strip()
    except:
        pass
    return result


class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(pretty_price))
    currency = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(pretty_address))
    description = scrapy.Field(output_processor=TakeFirst(), input_processor=Compose(pretty_description))
