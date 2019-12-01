# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Compose, Identity


def salary_spitter(salary):
    res = {'min_salary': None, 'max_salary': None, 'currency': None}
    if len(salary) == 2:
        res['min_salary'] = float(''.join(re.split('\s', salary[0])))
        res['currency'] = salary[1]
    elif len(salary) == 3:
        res['currency'] = salary[0]
        res['min_salary'] = float(salary[1])
    elif len(salary) == 4:
        res['currency'] = salary[0]
        res['min_salary'] = float(salary[1])
        res['max_salary'] = float(salary[2])
    elif len(salary) == 6:
        res['min_salary'] = float(''.join(re.split('\s', salary[0])))
        res['max_salary'] = float(''.join(re.split('\s', salary[4])))
        res['currency'] = salary[5]
    return res


class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    source = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(output_processor=TakeFirst(), input_processor=Compose(salary_spitter))
