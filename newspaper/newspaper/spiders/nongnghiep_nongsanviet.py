import scrapy


class NongnghiepNongsanvietSpider(scrapy.Spider):
    name = 'nongnghiep_nongsanviet'
    start_urls = ['https://nongsanviet.nongnghiep.vn/nong-san-viet-nong-nghiep-40/',
                    'https://nongsanviet.nongnghiep.vn/nong-san-the-gioi/',
                    'https://nongsanviet.nongnghiep.vn/organic/',
                    'https://nongsanviet.nongnghiep.vn/thi-truong/',
                    'https://nongsanviet.nongnghiep.vn/doanh-nghiep/']
    custom_settings = { 'FEED_URI': "nongnghiep_nongsanviet_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        count = 0
        id = -1
        v = -1

        post_urls = response.xpath('//h3[@class="main-title main-title-lager"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        post_urls_extra = response.xpath('//h4[@class="main-title main-title-lager"]//a/@href').extract()
        for url_item in post_urls_extra:
            yield scrapy.Request(url_item, callback=self.parse_post)

        if 'https://nongsanviet.nongnghiep.vn/nong-san-viet-nong-nghiep-40/' in response.url:
            start_url = 'https://nongsanviet.nongnghiep.vn/nong-san-viet-nong-nghiep-40/' 
            id = 190
            v = 0

        if 'https://nongsanviet.nongnghiep.vn/nong-san-the-gioi/' in response.url:
            start_url = 'https://nongsanviet.nongnghiep.vn/nong-san-the-gioi/'
            id = 243
            v = 24

        if 'https://nongsanviet.nongnghiep.vn/organic/' in response.url:
            start_url = 'https://nongsanviet.nongnghiep.vn/organic/'
            id = 192
            v = 57

        if 'https://nongsanviet.nongnghiep.vn/thi-truong/' in response.url:
            start_url = 'https://nongsanviet.nongnghiep.vn/thi-truong/'
            id = 246
            v = 19

        if 'https://nongsanviet.nongnghiep.vn/doanh-nghiep/' in response.url:
            start_url = 'https://nongsanviet.nongnghiep.vn/doanh-nghiep/'
            id = 247
            v = 38

        while count < 21:
            extent_url = "?mod=news&act=loadmore_cate&category_id=" + str(id) + "&page=" + str(count) + "&v=" + str(v)
            main_url = start_url + extent_url
            yield scrapy.Request(main_url, callback=self.parse)
            count = count + 1

    def parse_post(self, response):
        if response.xpath('//h1[@class="title_news"]//text()').get() is not None:
            print("Post URL: " + response.url)

            yield {
                'url': response.url,
                'title': response.xpath('//h1[@class="title_news"]//text()').get().strip(),
                'author': ' '.join(response.xpath('//div[@class="signature"]//text()').extract()).strip(),
                'date': ' '.join(response.xpath('//span[@class="time-detail"]//text()').extract()).strip(),
                'sapo': ' '.join(response.xpath('//div[@class="sapo"]//text()').extract()).strip(),
                'text': ' '.join(response.xpath('//div[@class="content_detail"]//text()').extract()).strip(),
            }
