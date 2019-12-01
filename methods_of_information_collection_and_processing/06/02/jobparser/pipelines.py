# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        # res = {}
        # res['source'] = item['source']
        # res['name'] = item['name']
        # res['link'] = item['link']
        # res['source'] = item['salary'][0]['']
        collection.insert_one(item)
        return item
