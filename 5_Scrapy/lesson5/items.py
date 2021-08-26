# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Lesson5Item(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()


class ToolsItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    article = scrapy.Field()
    photos = scrapy.Field()
