import scrapy
import pkgutil

class ThivienSpider(scrapy.Spider):
    name = 'thivien'
    start_urls = ['https://www.thivien.net/searchpoem.php']
    custom_settings = { 'FEED_URI': "thivien.net_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        data = pkgutil.get_data("nomscript", "resources/dictionary.txt")
        data = data.decode()

        # Read dictionary
        for line in data.split('\n'):
            # VNPoem=<word>
            list_post = response.url + "?Country=3&VNPoem=" + line.strip()
            yield scrapy.Request(list_post, callback=self.parse_list)

            # Title=<word>
            # TODO

            # Author=<word>
            # TODO

    def parse_list(self, response):
        print("List URL: " + response.url)
        base_url = "https://www.thivien.net"

        # Iterate list items
        list_posts = response.xpath('//div[@class="list-item"]//h4//a//@href').extract()
        if list_posts is not None:
            for item_post in list_posts:
                yield scrapy.Request(base_url + item_post, callback=self.parse_post)

        # Iterate pagination
        next_pages = response.xpath('//div[@class="page-content-main"]//p//span//a/@href').extract()
        if next_pages is not None:
            for item_page in next_pages:
                yield scrapy.Request(base_url + item_page, callback=self.parse_list)


    def parse_post(self, response):
        print("Post URL: " + response.url)

        yield {
            'url': response.url,
            'title': '\n'.join(response.xpath('//header[@class="page-header"]//h1//text()').extract()),
            'text': '\n'.join(response.xpath('//div[@class="poem-content"]//text()').extract()),
        }