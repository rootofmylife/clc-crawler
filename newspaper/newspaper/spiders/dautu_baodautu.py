import scrapy


class DautuBaodautuSpider(scrapy.Spider):
    name = 'dautu_baodautu'
    start_urls = ['https://baodautu.vn/dau-tu-d2/']
    custom_settings = { 'FEED_URI': "dautu_baodautu_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        count = 2

        post_urls = response.xpath('//a[@class="fs22 fbold"]/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        while count < 665:
            extent_url = "p" + str(count) 
            main_url = 'https://baodautu.vn/dau-tu-d2/' + extent_url
            yield scrapy.Request(main_url, callback=self.parse)
            count = count + 1

    def parse_post(self, response):
        print("Post URL: " + response.url)

        if response.xpath('//a[@class="author cl_green"]//text()').get() == None:
                author = ''
        else:
            author = response.xpath('//a[@class="author cl_green"]//text()').get().strip()

        yield {
            'url': response.url,
            'title': response.xpath('//div[@class="title-detail"]/text()').get().strip(),
            'author': author,
            'date': response.xpath('//span[@class="post-time"]//text()').get().strip(),
            'sapo': response.xpath('//div[@class="sapo_detail"]//text()').get().strip(),
            'text': ' '.join(response.xpath('//div[@id="content_detail_news"]//p//text()').extract()).strip(),
        }
