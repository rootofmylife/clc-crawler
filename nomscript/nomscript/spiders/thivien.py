import scrapy


class ThivienSpider(scrapy.Spider):
    name = 'thivien'
    allowed_domains = ['https://www.thivien.net/']
    start_urls = ['https://www.thivien.net/searchpoem.php?Country=3']
    custom_settings = { 'FEED_URI': "thivien.net_%(time)s.json",
                       'FEED_FORMAT': 'json'}

    def parse(self, response):
        pass
