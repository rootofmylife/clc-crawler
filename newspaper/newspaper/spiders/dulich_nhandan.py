import scrapy


class DulichNhandanSpider(scrapy.Spider):
    name = 'dulich_nhandan'
    start_urls = ['https://nhandan.com.vn/article/Paging?categoryId=1257&pageIndex=1&pageSize=15']
    custom_settings = { 'FEED_URI': "dulich_nhandan_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+\n\n")

        counter = 2

        post_urls = response.xpath('//div[@class="box-title"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request('https://nhandan.com.vn' + url_item, callback=self.parse_post)

        while counter < 250:
            main_url = 'https://nhandan.com.vn/article/Paging?categoryId=1257&pageIndex=' + str(counter) + '&pageSize=15'
            yield scrapy.Request(main_url, callback=self.parse)
            counter = counter + 1

    def parse_post(self, response):
        if response.xpath('//h1[@class="box-title-detail entry-title"]/text()').get() is not None:
            print("Post URL: " + response.url)

            if response.xpath('//div[@class="box-author uk-text-right uk-clearfix"]//strong/text()').get() == None:
                author = ''
            else:
                author = response.xpath('//div[@class="box-author uk-text-right uk-clearfix"]//strong/text()').get().strip()

            if response.xpath('//div[@class="box-des-detail this-one"]//p//text()').get() == None:
                sapo = ''
            else:
                sapo = response.xpath('//div[@class="box-des-detail this-one"]//p//text()').get().strip()

            yield {
                'url': response.url,
                'title': response.xpath('//h1[@class="box-title-detail entry-title"]/text()').get().strip(),
                'author': author,
                'date': response.xpath('//div[@class="box-date pull-left"]/text()').get().strip(),
                'sapo': sapo,
                'text': ' '.join(response.xpath('//div[contains(@class, "detail-content-body")]//p//text()').extract()).strip(),
            }
