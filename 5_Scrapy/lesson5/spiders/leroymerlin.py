import scrapy
from scrapy.http import HtmlResponse
from lesson5.items import ToolsItem


class leroymerlinSpider(scrapy.Spider):
    name = "leroymer"
    allowed_domains = ["leroymerlin.ru"]
    start_urls = ["https://leroymerlin.ru/catalogue/elektroinstrumenty/"]

    def parse(self, response: HtmlResponse):
        next_page = response.css("a[data-qa-pagination-item='right']::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

        tools = response.css("div.largeCard[data-qa-product] > a::attr(href)").extract()

        for link in tools:
            yield response.follow(link, callback=self.tools_parse)

    def tools_parse(self, response: HtmlResponse):
        item = ToolsItem()

        name = response.css(".card-data h1::text").extract_first()
        price = response.css(".primary-price span[slot='price']::text").extract_first()
        article = response.css("span[slot='article']::text").extract_first()
        photos = response.css("picture[slot='pictures'] img::attr(src)").extract()

        item["name"] = name
        item["price"] = price
        item["article"] = article
        item["photos"] = photos

        yield item
