import scrapy


class TaichinhThoibaotaichinhvietnamSpider(scrapy.Spider):
    name = 'taichinh_thoibaotaichinhvietnam'
    start_urls = ['http://thoibaotaichinhvietnam.vn/pages/nhip-song-tai-chinh-3.aspx',
                    'http://thoibaotaichinhvietnam.vn/pages/chung-khoan-5.aspx',
                    'http://thoibaotaichinhvietnam.vn/pages/tien-te-bao-hiem-6.aspx']
    custom_settings = { 'FEED_URI': "taichinh_thoibaotaichinhvietnam_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+\n\n")

        post_urls = response.xpath('//div[@class="component_content"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request('http://thoibaotaichinhvietnam.vn' + url_item, callback=self.parse_post)

        next_page = response.xpath('//div[@class="page-next"]//a/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request('http://thoibaotaichinhvietnam.vn' + next_page, callback=self.parse)

    def parse_post(self, response):
        if response.xpath('//div[@class="article-header"]//h1/text()').get() is not None:
            print("Post URL: " + response.url)

            if response.xpath('//div[@class="tacgia"]/text()').get() == None:
                author = ''
            else:
                author = response.xpath('//div[@class="tacgia"]/text()').get().strip()

            if response.xpath('//span[@class="date-time dtngaydang"]/text()').get() == None:
                date = ''
            else:
                date = response.xpath('//span[@class="date-time dtngaydang"]/text()').get().strip()

            yield {
                'url': response.url,
                'title': response.xpath('//div[@class="article-header"]//h1/text()').get().strip(),
                'author': author,
                'date': date,
                'sapo': response.xpath('//h2[@class="article-content02 article-content03"]//div//text()').get().strip(),
                'text': ' '.join(response.xpath('//div[@class="article-content article-content02"]//p//text()').extract()).strip(),
            }
