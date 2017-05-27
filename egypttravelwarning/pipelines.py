# -*- coding: utf-8 -*-

import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

from egypttravelwarning.items import TravelWarningItem


class MongoDBPipeline(object):

    def __init__(self):
        self.mongo_uri = "mongodb://%s:%s@%s:%s/%s" % (settings['MONGODB_USER'], settings['MONGODB_PASSWORD'], settings['MONGODB_SERVER'], settings['MONGODB_PORT'], settings['MONGODB_DB'])
        
        self.mongo_db = settings['MONGODB_DB']

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        if isinstance(item, TravelWarningItem):      
           self.db[settings['MONGODB_COLLECTION_TRAVELWARNINGS']].update({'url': item['url']}, dict(item), upsert=True)
           if settings['LOG_LEVEL'] == 'DEBUG':
              spider.logger.debug("{} added to MongoDB database!".format(item['url']))

        return item
        
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

