import scrapy


class ThuongmaiCongthuongSpider(scrapy.Spider):
    name = 'thuongmai_congthuong'
    start_urls = ['https://congthuong.vn/thuong-mai/xuat-xu-hang-hoa',
                    'https://congthuong.vn/thuong-mai/xuat-nhap-khau',
                    'https://congthuong.vn/thuong-mai/xuc-tien-thuong-mai',
                    'https://congthuong.vn/thuong-mai/phong-ve-thuong-mai',
                    'https://congthuong.vn/thuong-mai/thuong-hieu-quoc-gia',
                    'https://congthuong.vn/cong-nghe/thuong-mai-dien-tu',
                    'https://congthuong.vn/hoi-nhap/thong-tin-thuong-vu',
                    'https://congthuong.vn/hoi-nhap/hiep-dinh-evfta',
                    'https://congthuong.vn/hoi-nhap/quoc-te']
    custom_settings = { 'FEED_URI': "thuongmai_congthuong_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+\n\n")

        post_urls = response.xpath('//a[@class="article-title"]/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request(url_item, callback=self.parse_post)

        next_page = response.xpath('//div[@class="grNextPage __MB_ARTICLE_PAGING lt"]//a[last()-1]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):
        print("Post URL: " + response.url)

        if response.xpath('//p[@class="author"]/text()').get() == None:
            author = ''
        else:
            author = response.xpath('//p[@class="author"]/text()').get().strip()

        yield {
            'url': response.url,
            'title': response.xpath('//article[@class="article"]//h1/text()').get().strip(),
            'author': author,
            'date': response.xpath('//span[@class="bx-time lt"]/text()').get().strip(),
            'sapo': ' '.join(response.xpath('//div[@class="article-desc fw lt clearfix"]//text()').extract()).strip(),
            'text': ' '.join(response.xpath('//div[@class="__MASTERCMS_CONTENT_BODY clearfix"]//text()').extract()).strip(),
        }
