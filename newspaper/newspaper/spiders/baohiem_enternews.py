import scrapy


class BaohiemEnternewsSpider(scrapy.Spider):
    name = 'baohiem_enternews'
    allowed_domains = ['enternews.vn']
    start_urls = ['http://enternews.vn/bao-hiem-c103']
    custom_settings = { 'FEED_URI': "baohiem_enternews_%(time)s.json",
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
