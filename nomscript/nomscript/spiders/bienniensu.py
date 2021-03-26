import scrapy


class BienniensuSpider(scrapy.Spider):
    name = 'bienniensu'
    start_urls = ['https://bienniensu.com/lich-su-viet-nam/', 'https://bienniensu.com/lich_su_trung_quoc/']
    custom_settings={ 'FEED_URI': "bienniensu_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        post_urls = response.xpath('//header[@class="entry-header"]//h2[@class="entry-title"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        next_page = response.xpath('//a[@class="nextpostslink"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):
        print("Post URL: " + response.url)

        yield {
            'url': response.url,
            'title': response.xpath('//h1[@class="entry-title"]/text()').get(),
            'text': ' '.join(response.xpath('//div[@class="entry-content"]//text()').extract()),
        }