import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import re
from lesson5.items import ToolsItem


class leroymerlinSpider(scrapy.Spider):
    name = "leroymer"
    allowed_domains = ["leroymerlin.ru"]
    start_urls = ["https://leroymerlin.ru/catalogue/cirkulyarnye-pily/"]

    def parse(self, response: HtmlResponse):
        next_page = response.css("a[data-qa-pagination-item='right']::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

        tools = response.css("div.largeCard[data-qa-product] > a::attr(href)").extract()

        for link in tools:
            yield response.follow(link, callback=self.tools_parse)

    def tools_parse(self, response: HtmlResponse):
        item = ItemLoader(item=ToolsItem(), response=response)

        item.add_css("name", ".card-data h1::text")
        item.add_css(
            "price",
            ".primary-price span[slot='price']::text",
            MapCompose(lambda value: int(re.sub(r"\s", "", value)))
        )
        item.add_css("article", "span[slot='article']::text")
        item.add_css("photos", "picture[slot='pictures'] img::attr(src)")

        yield item.load_item()
