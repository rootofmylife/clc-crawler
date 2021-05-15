import scrapy


class NongnghiepDanvietSpider(scrapy.Spider):
    name = 'nongnghiep_danviet'
    start_urls = ['https://danviet.vn/'] # /nha-nong.htm
    custom_settings = { 'FEED_URI': "nongnghiep_datviet_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        count = 1

        post_urls = response.xpath('//h3//a[@class="title"]/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(response.urljoin(url_item), callback=self.parse_post)

        while count < 4435:
            extent_url = "timeline/1009/trang-" + str(count) + ".htm"
            main_url = 'https://danviet.vn/' + extent_url
            yield scrapy.Request(main_url, callback=self.parse)
            count = count + 1

    def parse_post(self, response):
        check_cate = response.xpath('//div[@class="title-main"]//a/@href').extract()

        if "/nha-nong.htm" in check_cate:
            print("Post URL: " + response.url)

            yield {
                'url': response.url,
                'title': response.xpath('//h1//span[@class="title"]/text()').get().strip(),
                'author': ' '.join(response.xpath('//div[@class="line-datetime"]//span[@class="anots"]//text()').extract()).strip(),
                'date': ' '.join(response.xpath('//div[@class="line-datetime"]//span[@data-role="publishdate"]//text()').extract()).strip(),
                'sapo': ' '.join(response.xpath('//div[@class="sapo"]//text()').extract()).strip(),
                'text': ' '.join(response.xpath('//div[@class="entry-body dtdefault clearfix"]//text()').extract()).strip(),
            }
