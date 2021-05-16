import scrapy


class NganhangTapchinganhangSpider(scrapy.Spider):
    name = 'nganhang_tapchinganhang'
    start_urls = ['http://tapchinganhang.com.vn/co-che-chinh-sach.htm',
                    'http://tapchinganhang.com.vn/hoat-dong-ngan-hang.htm',
                    'http://tapchinganhang.com.vn/cong-nghe-ngan-hang.htm',
                    'http://tapchinganhang.com.vn/nghien-cuu-trao-doi.htm']
    custom_settings = { 'FEED_URI': "nganhang_tapchinganhang_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+\n\n")

        counter = 1

        post_urls = response.xpath('//div[@class="new-gr"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        base_url = response.url.replace('.htm', '') + '/'

        while len(post_urls) != 0 and counter < 50:
            yield scrapy.Request(base_url + 'trang-' + str(counter) + '.htm', callback=self.parse)
            counter = counter + 1

    def parse_post(self, response):
        if response.xpath('//div[@class="cbe1e2d fRobotoB lh30 db fs24 pb15"]//h1/text()').get() is not None:
            print("Post URL: " + response.url)

            if response.xpath('//div[@class="noidung TextSize"]//strong/text()').get() == None:
                author = ''
            else:
                author = response.xpath('//div[@class="noidung TextSize"]//strong/text()').get().strip()

            if response.xpath('//div[@class="nddes fRobotoB lh22 pb20 "]//text()').get() == None:
                sapo = ''
            else:
                sapo = response.xpath('//div[@class="nddes fRobotoB lh22 pb20 "]//text()').get().strip()

            yield {
                'url': response.url,
                'title': response.xpath('//div[@class="cbe1e2d fRobotoB lh30 db fs24 pb15"]//h1/text()').get().strip(),
                'author': author,
                'date': response.xpath('//div[@class="thongke-ngay"]//span/text()').get().strip(),
                'sapo': sapo,
                'text': ' '.join(response.xpath('//div[@class="noidung TextSize"]//text()').extract()).strip(),
            }
