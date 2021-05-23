import scrapy


class TaichinhEnternewsSpider(scrapy.Spider):
    name = 'taichinh_enternews'
    start_urls = ['https://enternews.vn/chung-khoan-c124',
                    'https://enternews.vn/tien-te-c249',
                    'https://enternews.vn/tai-chinh-doanh-nghiep-c250',
                    'https://enternews.vn/thi-truong-chung-khoan-c264',
                    'https://enternews.vn/co-phieu-c265',
                    'https://enternews.vn/vang-c276',
                    'https://enternews.vn/tai-chinh-so-c309',
                    'https://enternews.vn/chuyen-de-c310',
                    'https://enternews.vn/tu-van-tai-chinh-c311']
    custom_settings = { 'FEED_URI': "doanhnghiep_enternews_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+\n\n")

        post_urls = response.xpath('//h2[@class="post-title"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        next_page = response.xpath('//div[@class="pull-right"]//a[@class="btn btn-xs font-14 btn-primary"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):
        if response.xpath('//h1[@class="post-title main-title"]/text()').get() is not None:
            print("Post URL: " + response.url)

            if response.xpath('//strong[@class="post-author-fs"]/text()').get() == None:
                author = ''
            else:
                author = response.xpath('//strong[@class="post-author-fs"]/text()').get().strip()

            yield {
                'url': response.url,
                'title': response.xpath('//h1[@class="post-title main-title"]/text()').get().strip(),
                'author': author,
                'date': response.xpath('//div[@class="post-author cl"]//span/text()').get().strip(),
                'sapo': response.xpath('//h2[@class="post-sapo"]//strong//text()').get().strip(),
                'text': ' '.join(response.xpath('//div[@class="post-content "]//p//text()').extract()).strip(),
            }
