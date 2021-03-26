import scrapy
import js2xml

class VnthuquanSpider(scrapy.Spider):
    name = 'vnthuquan'
    start_urls = ['https://vnthuquan.net/Tho/', 'https://vnthuquan.net/truyen/']
    custom_settings={ 'FEED_URI': "vnthuquan_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("+===========+")
        print("URL: " + response.url)
        print("+===========+")

        form_data = self.validate(response)

        post_urls = response.xpath('//li[@class="menutruyen"]//a/@href').extract()
        for url_item in post_urls:
            # js2xml allows us to parse the JS function and params, and so to grab the __EVENTTARGET
            js_xml  = js2xml.parse(url_item)
            _id = js_xml.xpath("//identifier[@name='WebForm_PostBackOptions']/following-sibling::arguments/string[starts-with(.,'ctl')]")[0]
            form_data["__EVENTTARGET"] = _id.text

            url_diputado = response.urljoin(url_item)
            # The proper way to send a POST in scrapy is by using the FormRequest
            yield scrapy.FormRequest(url=url_diputado, formdata=form_data, callback=self.parse_post, method='POST')
            

            # url_merge = response.urljoin(url_item)
            # yield scrapy.Request(url_merge, callback=self.parse_post)

        next_pages = response.xpath('//div/h1//a/@href').extract()
        for url_item in next_pages:
            yield scrapy.Request(url=response.urljoin(url_item), callback=self.parse)

    def parse_post(self, response):
        print("Post URL: " + response.url)

        title = ""
        if response.xpath('//span[@class="chuto40"]/text()'):
            title = response.xpath('//span[@class="chuto40"]/text()').get()

        if response.xpath('//div[@class="chuto30a"]/text()'):
            title = response.xpath('//div[@class="chuto30a"]/text()').get()

        yield {
            'url': response.url,
            'title': title,
            'text': ' '.join(response.xpath('//div[@class="truyen_text"]//text()').extract()),
        }

    def validate(self, source):
         # these fields are the minimum required as cannot be hardcoded
        data = {"__VIEWSTATEGENERATOR": source.xpath("//*[@id='__VIEWSTATEGENERATOR']/@value")[0].extract(),
                "__EVENTVALIDATION": source.xpath("//*[@id='__EVENTVALIDATION']/@value")[0].extract(),
                "__VIEWSTATE": source.xpath("//*[@id='__VIEWSTATE']/@value")[0].extract(),
                " __REQUESTDIGEST": source.xpath("//*[@id='__REQUESTDIGEST']/@value")[0].extract()}
        return data
