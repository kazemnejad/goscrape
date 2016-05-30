import scrapy
from scrapy.selector import Selector
class CafeBazaarSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["cafebazaar.ir"]
    start_urls = [
        "https://cafebazaar.ir/cat/?l=fa&partial=true"
    ]
    url_global=""
    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'


        for url in response.xpath('//a/@href').extract():
            yield {"status":"cat" , "cat":url.split('/')[-2]}

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request('https://cafebazaar.ir'+url, callback=self.find_more_app)
            print 'https://cafebazaar.ir'+url
    def parseApp(self, response):
        print '############'
        print 'salam'
        print "############"

    def find_more_app(self,response):
        dic={}
        for url in response.xpath('//a/@href').extract():
            if ("new" in url) and ("best" not in url)and("list" in url):
                url=url.replace(" ","")
                self.url_global=url+'&partial=true'
                yield scrapy.Request('https://cafebazaar.ir'+url+'&partial=true',callback=self.find_all_app)
                print 'https://cafebazaar.ir'+url+'&partial=true'

    def find_all_app(self,response):
        i=0;
        urls=response.xpath('//a/@href').extract()
        print "***************"
        print response.body
        while True:
            if i%24 ==0 :
                scrapy.Request('https://cafebazaar.ir'+self.url_global+'&p='+str(i),callback=self.find_all_app())

            url=urls[i]
            print "***********"
            print url
            print "***********"
            scrapy.Request('https://cafebazaar.ir'+url,callback=self.see_app_details)
            if url=="" :
                break
            i+=1
    def see_app_details(self,response):
        spans=response.xpath('//span/text()').extract()

