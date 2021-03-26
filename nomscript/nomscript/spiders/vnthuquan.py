import scrapy


class VnthuquanSpider(scrapy.Spider):
    name = 'vnthuquan'
    start_urls = ['https://vnthuquan.net/Tho/', 'https://vnthuquan.net/truyen/']
    custom_settings={ 'FEED_URI': "vnthuquan_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        post_urls = response.xpath('//li[@class="menutruyen"]//a/@href').extract()
        for url_item in post_urls:
            url_merge = response.urljoin(url_item)
            yield scrapy.Request(url_item, callback=self.parse_post)

        # website not stable, will update later
        next_pages = response.xpath('//div/h1//a/@href').extract()
        for url_item in next_pages:
            yield scrapy.Request(url=response.urljoin(url_item), callback=self.parse)

    def parse_post(self, response):
        print("Post URL: " + response.url)

        title = ""
        if response.xpath('//span[@class="chuto40"]/text()'):
            title = response.xpath('//span[@class="chuto40"]/text()').get()

        if response.xpath('//div[@class="chuto30a"]/text()'):
            title = response.xpath('//div[@class="chuto30a"]/text()').get()

        yield {
            'url': response.url,
            'title': title,
            'text': ' '.join(response.xpath('//div[@class="truyen_text"]//text()').extract()),
        }
