import scrapy


class BienniensuSpider(scrapy.Spider):
    name = 'bienniensu'
    allowed_domains = ['https://bienniensu.com/']
    start_urls = ['http://https://bienniensu.com//']

    def parse(self, response):
        pass
