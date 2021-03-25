import scrapy


class VnthuquanSpider(scrapy.Spider):
    name = 'vnthuquan'
    allowed_domains = ['https://vnthuquan.net/']
    start_urls = ['http://https://vnthuquan.net//']

    def parse(self, response):
        pass
