import scrapy

# bypass cloudflare: https://stackoverflow.com/questions/35891631/how-to-bypass-cloudflare-using-scrapy
class NongnghiepNongnghiepSpider(scrapy.Spider):
    name = 'nongnghiep_nongnghiep'
    start_urls = ['https://nongnghiep.vn/thoi-su-nong-nghiep/', # id: 80; max: 20
                    'https://nongnghiep.vn/kinh-te-thi-truong/', # id: 80; max: 20
                    'https://nongnghiep.vn/tai-co-cau-nong-nghiep/', # id: 135
                    'https://nongnghiep.vn/thuy-san/', # id: 22
                    'https://nongnghiep.vn/lam-nghiep/'] # id: 201
    custom_settings = { 'FEED_URI': "nongnghiep_nongnghiep_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        count = 0
        id = -1
        v = -1

        post_urls = response.xpath('//h4[@class="main-title main-title-sizable"]//a/@href').extract()

        if 'https://nongnghiep.vn/thoi-su-nong-nghiep/' in response.url:
            for url_item in post_urls:
                yield scrapy.Request(url_item, callback=self.parse_post_thoi_su)

        if 'https://nongnghiep.vn/kinh-te-thi-truong/' in response.url:
            for url_item in post_urls:
                yield scrapy.Request(url_item, callback=self.parse_post_kinh_te)

        if 'https://nongnghiep.vn/tai-co-cau-nong-nghiep/' in response.url:
            for url_item in post_urls:
                yield scrapy.Request(url_item, callback=self.parse_post_tai_co_cau)

        if 'https://nongnghiep.vn/thuy-san/' in response.url:
            for url_item in post_urls:
                yield scrapy.Request(url_item, callback=self.parse_post_thuy_san)

        if 'https://nongnghiep.vn/lam-nghiep/' in response.url:
            for url_item in post_urls:
                yield scrapy.Request(url_item, callback=self.parse_post_lam_nghiep)

        if 'https://nongnghiep.vn/thoi-su-nong-nghiep/' in response.url:
            start_url = 'https://nongnghiep.vn/thoi-su-nong-nghiep/' 
            id = 80
            v = 22

        if 'https://nongnghiep.vn/kinh-te-thi-truong/' in response.url:
            start_url = 'https://nongnghiep.vn/kinh-te-thi-truong/'
            id = 80
            v = 27

        if 'https://nongnghiep.vn/tai-co-cau-nong-nghiep/' in response.url:
            start_url = 'https://nongnghiep.vn/tai-co-cau-nong-nghiep/'
            id = 135
            v = 6

        if 'https://nongnghiep.vn/thuy-san/' in response.url:
            start_url = 'https://nongnghiep.vn/thuy-san/'
            id = 22
            v = 50

        if 'https://nongnghiep.vn/lam-nghiep/' in response.url:
            start_url = 'https://nongnghiep.vn/lam-nghiep/'
            id = 201
            v = 41

        while count < 21:
            extent_url = "?mod=news&act=loadmore_cate&category_id=" + str(id) + "&page=" + str(count) + "&v=" + str(v)
            main_url = start_url + extent_url
            yield scrapy.Request(main_url, callback=self.parse)
            count = count + 1

    def parse_post_thoi_su(self, response):
        if response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get() is not None:
            print("Post URL: " + response.url)

            yield {
                'url': response.url,
                'title': 'thoisu:' + response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get().strip(),
                'author': ' '.join(response.xpath('//p[@class="content-author"]//text()').extract()).strip(),
                'date': ' '.join(response.xpath('//span[@class="time-detail time-detail-mobile"]//text()').extract()).strip(),
                'sapo': ' '.join(response.xpath('//p[@class="main-intro detail-intro"]//text()').extract()).strip(),
                'text': ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip(),
            }

    def parse_post_kinh_te(self, response):
        if response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get() is not None:
            print("Post URL: " + response.url)

            yield {
                'url': response.url,
                'title': 'kinhte:' + response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get().strip(),
                'author': ' '.join(response.xpath('//p[@class="content-author"]//text()').extract()).strip(),
                'date': ' '.join(response.xpath('//span[@class="time-detail time-detail-mobile"]//text()').extract()).strip(),
                'sapo': ' '.join(response.xpath('//p[@class="main-intro detail-intro"]//text()').extract()).strip(),
                'text': ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip(),
            }
    
    def parse_post_tai_co_cau(self, response):
        if response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get() is not None:
            print("Post URL: " + response.url)

            yield {
                'url': response.url,
                'title': 'taicocau:' + response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get().strip(),
                'author': ' '.join(response.xpath('//p[@class="content-author"]//text()').extract()).strip(),
                'date': ' '.join(response.xpath('//span[@class="time-detail time-detail-mobile"]//text()').extract()).strip(),
                'sapo': ' '.join(response.xpath('//p[@class="main-intro detail-intro"]//text()').extract()).strip(),
                'text': ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip(),
            }

    def parse_post_thuy_san(self, response):
        if response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get() is not None:
            print("Post URL: " + response.url)

            yield {
                'url': response.url,
                'title': 'thuysan:' + response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get().strip(),
                'author': ' '.join(response.xpath('//p[@class="content-author"]//text()').extract()).strip(),
                'date': ' '.join(response.xpath('//span[@class="time-detail time-detail-mobile"]//text()').extract()).strip(),
                'sapo': ' '.join(response.xpath('//p[@class="main-intro detail-intro"]//text()').extract()).strip(),
                'text': ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip(),
            }

    def parse_post_lam_nghiep(self, response):
        if response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get() is not None:
            print("Post URL: " + response.url)

            yield {
                'url': response.url,
                'title': 'lamnghiep:' + response.xpath('//h1[@class="main-title main-title-super detail-title"]//text()').get().strip(),
                'author': ' '.join(response.xpath('//p[@class="content-author"]//text()').extract()).strip(),
                'date': ' '.join(response.xpath('//span[@class="time-detail time-detail-mobile"]//text()').extract()).strip(),
                'sapo': ' '.join(response.xpath('//p[@class="main-intro detail-intro"]//text()').extract()).strip(),
                'text': ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip(),
            }
