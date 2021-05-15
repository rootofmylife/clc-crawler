import scrapy


class DoanhnghiepDoanhnghieptiepthiSpider(scrapy.Spider):
    name = 'doanhnghiep_doanhnghieptiepthi'
    start_urls = ['https://doanhnghieptiepthi.vn/doanh-nghiep.htm']
    custom_settings = { 'FEED_URI': "doanhnghiep_doanhnghieptiepthi_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        count = 1

        post_urls = response.xpath('//h3//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request('http://doanhnghieptiepthi.vn' + url_item, callback=self.parse_post)

        while count < 367:
            extent_url = "doanh-nghiep/trang-" + str(count) + ".htm"
            main_url = 'http://doanhnghieptiepthi.vn/' + extent_url
            yield scrapy.Request(main_url, callback=self.parse)
            count = count + 1

    def parse_post(self, response):
        print("Post URL: " + response.url)

        if response.xpath('//b[@class="detail__author"]//text()').get() == None:
            author = ''
        else:
            author = response.xpath('//b[@class="detail__author"]//text()').get().strip()

        yield {
            'url': response.url,
            'title': response.xpath('//h1[@class="detail__title"]/text()').get().strip(),
            'author': author,
            'date': response.xpath('//span[@data-role="publishdate"]//text()').get().strip(),
            'sapo': ' '.join(response.xpath('//div[@class="detail__sapo"]//text()').extract()).strip(),
            'text': ' '.join(response.xpath('//div[@class="detail__content afcbc-body"]//text()').extract()).strip(),
        }
