import scrapy


class BdsReatimesSpider(scrapy.Spider):
    name = 'bds_reatimes'
    start_urls = ['https://reatimes.vn/cafe-bds-c10.html',
                    'https://reatimes.vn/thi-truong-du-bao-c3.html',
                    'https://reatimes.vn/tai-chinh-bat-dong-san-c26.html']
    custom_settings = { 'FEED_URI': "bds_reatimes_%(time)s.json",
                        'FEED_FORMAT': 'json',
                        'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        post_urls = response.xpath('//div[@class="knswli-right"]//h3//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        next_page = response.xpath('//ul[@class="pager clearfix mb-15"]//a/@href').extract()[-1]
        if next_page is not None and len(post_urls) > 0:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):
        if response.xpath('//h1[contains(@class, "content-title")]/text()').get() is not None:
            print("Post URL: " + response.url)

            if response.xpath('//p[contains(@class, "content-author")]//a//text()').get() == None:
                author = ''
            else:
                author = response.xpath('//p[contains(@class, "content-author")]//a//text()').get().strip()

            sapo = ' '.join(response.xpath('//h2[contains(@class, "content-sapo")]//text()').extract()).strip()

            if len(sapo) == 0:
                sapo = response.xpath('//p[contains(@class, "content-sapo")]//text()').get().strip()

            yield {
                'url': response.url,
                'title': response.xpath('//h1[contains(@class, "content-title")]/text()').get().strip(),
                'author': author,
                'date': ' '.join(response.xpath('//div[contains(@class, "category-time") or contains(@class, "content-time")]//text()').extract()).strip(),
                'sapo': sapo,
                'text': ' '.join(response.xpath('//div[contains(@class, "content-body")]//text()').extract()).strip(),
            }
