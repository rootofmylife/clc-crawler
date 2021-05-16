import scrapy


class BaohiemTapchitaichinhSpider(scrapy.Spider):
    name = 'baohiem_tapchitaichinh'
    start_urls = ['https://tapchitaichinh.vn/bao-hiem/']
    custom_settings = { 'FEED_URI': "baohiem_tapchitaichinh_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+\n\n")

        counter = 1

        post_urls = response.xpath('//h4[@class="story__heading"]//a/@href').extract()
        for url_item in post_urls:
            if url_item.startswith('/bao-hiem'):
                yield scrapy.Request('https://tapchitaichinh.vn' + url_item, callback=self.parse_post)

        while counter < 33:
            yield scrapy.Request('https://tapchitaichinh.vn/bao-hiem/' + '?trang=' + str(counter), callback=self.parse)
            counter = counter + 1

    def parse_post(self, response):
        if response.xpath('//div[@class="article__header"]//h1/text()').get() is not None:
            print("Post URL: " + response.url)

            if response.xpath('//p[@class="author source-footer"]/text()').get() == None:
                author = ''
            else:
                author = response.xpath('//p[@class="author source-footer"]/text()').get().strip()

            yield {
                'url': response.url,
                'title': response.xpath('//div[@class="article__header"]//h1/text()').get().strip(),
                'author': author,
                'date': response.xpath('//div[@class="article__meta"]//time/text()').get().strip(),
                'sapo': response.xpath('//h2[@class="article__sapo"]//text()').get().strip(),
                'text': ' '.join(response.xpath('//div[@class="article__body"]//text()').extract()).strip(),
            }
