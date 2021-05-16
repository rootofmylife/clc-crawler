import scrapy


class DulichBvhttdlSpider(scrapy.Spider):
    name = 'dulich_bvhttdl'
    start_urls = ['https://bvhttdl.gov.vn/du-lich.htm']
    custom_settings = { 'FEED_URI': "dulich_bvhttdl_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+\n\n")

        post_urls = response.xpath('//div[@class="content-right left"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        next_page = response.xpath('//li[@class="pager_next"]//a/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request("https://bvhttdl.gov.vn" + next_page, callback=self.parse)

    def parse_post(self, response):
        print("Post URL: " + response.url)

        if response.xpath('//p[@class="author"]/text()').get() == None:
            author = ''
        else:
            author = response.xpath('//p[@class="author"]/text()').get().strip()

        yield {
            'url': response.url,
            'title': response.xpath('//h2[@class="title"]/text()').get().strip(),
            'author': author,
            'date': response.xpath('//span[@class="time margin-bottom"]/text()').get().strip(),
            'sapo': response.xpath('//p[@class="sapo"]//text()').get().strip(),
            'text': ' '.join(response.xpath('//div[@class="entry-body"]//text()').extract()).strip(),
        }
