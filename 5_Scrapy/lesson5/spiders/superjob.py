import scrapy
from scrapy.http import HtmlResponse
from lesson5.items import Lesson5Item
from lesson5.spiders.utils import get_info_salary


class superjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo[t][0]=4']

    def parse(self, response: HtmlResponse):
        next_page = response.css("a.f-test-link-Dalshe[rel='next']::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css(
            ".f-test-search-result-item .f-test-vacancy-item a[class*='f-test-link'][href*='/vakansii']::attr(href)"
        ).extract()

        for link in vacancy:
            yield response.follow(f'https://www.superjob.ru{link}', callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        item = Lesson5Item()

        name = response.css('.f-test-vacancy-base-info h1::text').extract_first()
        salary = response.xpath(
            "//div[contains(@class, 'f-test-vacancy-base-info')]/div[2]/div/div/div/span/span[1]/span//text()"
        ).extract()
        salary = ' '.join([str(element) for element in salary])
        salary = get_info_salary(salary)
        min_salary = salary["min"]
        max_salary = salary["max"]
        url = response.url
        source = "superjob.ru"

        item["name"] = name
        item["url"] = url
        item["source"] = source

        if min_salary != "":
            item["min_salary"] = min_salary

        if max_salary != "":
            item["max_salary"] = max_salary

        yield item
