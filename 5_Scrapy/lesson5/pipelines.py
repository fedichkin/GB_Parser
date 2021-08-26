import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class Lesson5Pipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy_280

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item


class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(f'{img}')
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
