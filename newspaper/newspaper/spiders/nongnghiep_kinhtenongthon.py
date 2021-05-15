import scrapy


class NongnghiepKinhtenongthonSpider(scrapy.Spider):
    name = 'nongnghiep_kinhtenongthon'
    start_urls = ['https://kinhtenongthon.vn/nghien-cuu-thuc-tien.html',
                    'https://kinhtenongthon.vn/kinh-te-phat-trien.html',
                    'https://kinhtenongthon.vn/vacvina---kinh-te-vac-thoi-4.0.html',
                    'https://kinhtenongthon.vn/360-nong-thon-moi.html',
                    'https://kinhtenongthon.vn/thi-truong.html',
                    'https://kinhtenongthon.vn/qua-cong-lang.html']
    custom_settings = { 'FEED_URI': "nongnghiep_kinhtenongthon_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        post_urls = response.xpath('//p[@class="title mb0"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            'url': response.url,
            'title': response.xpath('//h1[@class="fs-21"]/text()').get().strip(),
            'author': ' '.join(response.xpath('//div[@class="authors text-right font-bold"]//text()').extract()).strip(),
            'date': ' '.join(response.xpath('//span//time[@class="friendly"]//text()').extract()[:2]).strip(),
            'sapo': ' '.join(response.xpath('//p[@class="mb0"]//text()').extract()).strip(),
            'text': ' '.join(response.xpath('//article[@class="article-detail"]//text()').extract()).strip(),
        }
