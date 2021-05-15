import scrapy


class CongnghiepTapchicongthuongSpider(scrapy.Spider):
    name = 'congnghiep_tapchicongthuong'
    start_urls = ['http://tapchicongthuong.vn/hashtag/cong-nghiep-19.htm']
    custom_settings = { 'FEED_URI': "congnghiep_tapchicongthuong_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+\n\n")

        post_urls = response.xpath('//h3[@class="title title-2 m-0"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request('https://tapchicongthuong.vn' + url_item, callback=self.parse_post)

        next_page = response.xpath('//div[@class="pagination"]//a[@class="btn next"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request('https://tapchicongthuong.vn' + next_page, callback=self.parse)

    def parse_post(self, response):
        print("Post URL: " + response.url)
        # check_cate = response.xpath('//h2[@class="sub-heading-title"]//a//text()').extract()

        # if "Công nghiệp" in check_cate:
        #     print("Post URL: " + response.url)

        if response.xpath('//div[@class="author"]/text()').get() == None:
            author = ''
        else:
            author = response.xpath('//div[@class="author"]/text()').get().strip()

        yield {
            'url': response.url,
            'title': response.xpath('//h1[@class="post-title"]/text()').get().strip(),
            'author': author,
            'date': ' '.join(response.xpath('//div[@class="col-sm-6 post-date"]/text()').extract()).strip(),
            'sapo': ' '.join(response.xpath('//div[@class="sapo"]//text()').extract()).strip(),
            'text': ' '.join(response.xpath('//div[@class="post-content"]//text()').extract()).strip(),
        }
