import scrapy


class BdsVneconomySpider(scrapy.Spider):
    name = 'bds_vneconomy'
    start_urls = ['https://vneconomy.vn/dia-oc.htm']
    custom_settings = { 'FEED_URI': "bds_vneconomy_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        count = 2

        post_urls = response.xpath('//h3[@class="story__title"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request('https://vneconomy.vn' + url_item, callback=self.parse_post)

        while count < 71:
            extent_url = "?trang=" + str(count) 
            main_url = 'https://vneconomy.vn/dia-oc.htm' + extent_url
            yield scrapy.Request(main_url, callback=self.parse)
            count = count + 1

    def parse_post(self, response):
        print("Post URL: " + response.url)

        if response.xpath('//div[@class="detail__author"]//strong//text()').get() == None:
            author = ''
        else:
            author = response.xpath('//div[@class="detail__author"]//strong//text()').get().strip()

        if response.xpath('//h2[@class="detail__summary"]//text()').get() == None:
            sapo = ''
        else:
            sapo = response.xpath('//h2[@class="detail__summary"]//text()').get().strip()

        yield {
            'url': response.url,
            'title': response.xpath('//h1[@class="detail__title"]/text()').get().strip(),
            'author': author,
            'date': response.xpath('//div[@class="detail__meta"]//text()').get().strip(),
            'sapo': sapo,
            'text': ' '.join(response.xpath('//div[@class="detail__content"]//text()').extract()).strip(),
        }
