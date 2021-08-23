import scrapy
from scrapy.http import HtmlResponse
from lesson5.items import Lesson5Item
from lesson5.spiders.utils import get_info_salary


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python&area=1']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a[data-qa="pager-next"]::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css('.vacancy-serp-item .resume-search-item__name a::attr(href)').extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        item = Lesson5Item()

        name = response.css('div.vacancy-title h1::text').extract_first()
        salary = response.css('div.vacancy-title p.vacancy-salary span::text').extract_first()
        salary = get_info_salary(salary)
        min_salary = salary["min"]
        max_salary = salary["max"]
        url = response.url
        source = "hh.ru"

        item["name"] = name
        item["url"] = url
        item["source"] = source

        if min_salary != "":
            item["min_salary"] = min_salary

        if max_salary != "":
            item["max_salary"] = max_salary

        yield item
