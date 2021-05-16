import scrapy


class DulichVietnamtourismSpider(scrapy.Spider):
    name = 'dulich_vietnamtourism'
    start_urls = ['https://vietnamtourism.gov.vn/index.php/cat/45',
                    'https://vietnamtourism.gov.vn/index.php/cat/55',
                    'https://vietnamtourism.gov.vn/index.php/cat/60',
                    'https://vietnamtourism.gov.vn/index.php/cat/65',
                    'https://vietnamtourism.gov.vn/index.php/cat/15']
    custom_settings = { 'FEED_URI': "dulich_vietnamtourism_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        post_urls = response.xpath('//a[@class="block-item-title d-xl-none d-lg-none d-md-block"]/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        next_page = response.xpath('//div[@class="next"]//a/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):
        print("Post URL: " + response.url)

        if response.xpath('//div[@class="items-source"]//text()').get() == None:
                author = ''
        else:
            author = response.xpath('//div[@class="items-source"]//text()').get().strip()

        yield {
            'url': response.url,
            'title': response.xpath('//div[@class="items-title"]/text()').get().strip(),
            'author': author,
            'date': response.xpath('//div[@class="items-info-update"]//span//text()').get().strip(),
            'sapo': response.xpath('//h2[@class="summery"]//text()').get().strip(),
            'text': ' '.join(response.xpath('//div[@id="items-detail"]//p//text()').extract()).strip(),
        }
