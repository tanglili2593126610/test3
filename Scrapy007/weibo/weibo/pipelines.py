# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from weibo.items import WeiboItem
import pymongo

class WeiboPipeline(object):

    def process_time(self,datatime):   # 自定义方法，对爬取下来的时间进行格式修改。
        pass

    def process_item(self, item, spider):
        if isinstance(item,WeiboItem):
            if item.get('content'):
                item['content'] = item['content'].lstrip(':').strip()
            if item.get('posted_at'):
                item['posted_at'] = item['posted_at'].strip()
                item['posted_at'] = self.process_time(item['posted_at'])
        return item


class MongoPipeline(object):
    def __init__(self,uri,db):
        self.uri = uri
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('MONGO_URI'),
            db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[self.db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        self.db[item.table_name].update({'id':item.get('id')},{'$set':dict(item)},True)
        return item
