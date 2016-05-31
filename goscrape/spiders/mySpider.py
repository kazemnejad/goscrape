import scrapy
from numpy.core.fromnumeric import size
from scrapy.selector import Selector


class CafeBazaarSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["cafebazaar.ir"]
    start_urls = [
        "https://cafebazaar.ir/cat/?l=en&partial=true"
        # "https://cafebazaar.ir/app/com.blackstarteam.DoX/?l=en"
    ]
    url_global = ""

    def parse(self, response):

        filename = response.url.split("/")[-2] + '.html'

        for url in response.xpath('//a/@href').extract():
            yield {"status": "cat", "item": {'slug': url.split('/')[-2]}}

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request('https://cafebazaar.ir' + url, callback=self.find_more_app)

    def find_more_app(self, response):
        for url in response.xpath('//a/@href').extract():
            if ("new" in url) and ("best" not in url) and ("list" in url):
                url = url.replace(" ", "")
                url = url.replace("\n", "")
                self.url_global = url + '&partial=true'
                yield scrapy.Request('https://cafebazaar.ir' + url + '&partial=true', callback=self.find_all_app)

    def find_all_app(self, response):
        i = 0
        urls = response.xpath('//a/@href').extract()
        while True:
            if i % 24 == 0:
                yield scrapy.Request('https://cafebazaar.ir' + self.url_global + '&p=' + str(i),
                                     callback=self.find_all_app)
            try:
                url = urls[i]
            except:
                break
            url = url.replace(" ", "")
            url = url.replace("\n", "")
            yield scrapy.Request('https://cafebazaar.ir' + url, callback=self.see_app_details)
            i += 1

    def see_app_details(self, response):
        dic = {}
        category = response.xpath("//span[@itemprop='applicationSubCategory']/text()").extract_first()
        version = ''.join(response.xpath("//span[@itemprop='softwareVersion']/text()").extract())
        act_install = ''.join(
            response.xpath("//div[@class='col-sm-4']/div/span[@class='pull-right']/span/text()").extract())
        size = ''.join(response.xpath("//meta[@itemprop='fileSize']/@content").extract())
        price = ''.join(response.xpath("//meta[@itemprop='price']/@content").extract())
        rate = ''.join(response.xpath("//div[@class='rating-fill']/@style").extract())
        name = ''.join(response.xpath("//h1[@itemprop='name']/text()").extract())
        author = ''.join(response.xpath("//div[@itemprop='author']/a/span/text()").extract())
        component = response.url.split("/")[-2]
        icon = ''.join(response.xpath("//img[@class='app-img']/@src").extract())

        version = version.replace("\n", "")
        version = version.strip()
        size = size.replace("\n", "")
        size = size.strip()
        act_install = act_install.replace("less than ", "")
        act_install = act_install.replace(",", "")
        act_install = act_install.replace("+", "")
        removeDict = {'width': 10, '100%': 1, '80%': 1, '60%': 1, '40%': 1, '20%': 1}
        for i in removeDict:
            rate = rate.replace(i, '', removeDict[i])
            rate = rate.replace(':', '')
        rate = rate.strip()
        rate = rate.replace("\n", "")
        rate = rate.replace("%", "")
        rate = int(rate)
        name = name.replace('\n', '')
        name = name.strip()
        icon = icon.replace('\n','')
        icon = icon.strip()

        dic['category'] = category
        dic['version'] = version
        try:
            dic['act_install'] = int(act_install)
        except(ValueError):
            print "kose ammat "
        dic['size'] = int(size)
        dic['price'] = int(price)
        dic['name'] = name
        dic['author'] = author
        dic['component'] = component
        dic['icon'] = icon
        yield {"status": "app", 'item': dic}
