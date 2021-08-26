from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson5 import settings
from lesson5.spiders.hhru import HhruSpider
from lesson5.spiders.superjob import superjobSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(superjobSpider)
    process.start()
