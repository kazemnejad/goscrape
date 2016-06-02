# -*- coding: utf8 -*-

import random
from _mysql import result

import scrapy
import string
import re


class CafeBazaarSpider(scrapy.Spider):
    name = "cafebazaar"
    allowed_domains = ["cafebazaar.ir"]
    start_urls = [
        "https://cafebazaar.ir/cat/?l=fa&partial=true"
    ]
    url_global = ""

    def parse(self, response):
        for url in response.xpath('//a').extract():
            url = url.replace('\n', '')
            url = url.strip()
            cat_slug = re.match(r'.*cat\/(.*)\/\?.*$', url, re.X).groups()[0]
            cat_name = re.match(r'.*\>(.*)\<.*$', url, re.X).groups()[0]
            print "categoris app", cat_name.strip(), cat_slug
            yield {"status": "cat", "item": {'slug': cat_slug, 'name': cat_name}}
        i = 0
        for url in response.xpath('//a/@href').extract():
            print 'categoris url', 'https://cafebazaar.ir' + url, i
            i += 1
            yield scrapy.Request('https://cafebazaar.ir' + url, callback=self.find_more_app)

    def find_more_app(self, response):
        # find the more app button in the page
        for url in response.xpath('//a/@href').extract():
            if ("new" in url) and ("best" not in url) and ("list" in url):
                url = url.replace(" ", "")
                url = url.replace("\n", "")
                self.url_global = url + '&partial=true'
                print 'url new-app', 'https://cafebazaar.ir' + url + '&partial=true'
                yield scrapy.Request('https://cafebazaar.ir' + url + '&partial=true', callback=self.find_all_app)
        print 'self.global', self.url_global

    def find_all_app(self, response):
        # find all apps data
        pattern = re.compile(r'(&p=)(\d*)')
        response_url = re.search(pattern, response.url)
        if response_url:
            url_p = int(response_url.groups()[1])
        else:
            url_p = 0
        i = url_p
        urls = response.xpath('//a/@href').extract()

        while True:
            if i % 24 == 0:
                if response_url:
                    target_url = re.sub(pattern, '&p=' + str(i), response.url)
                else:
                    target_url = response.url + '&p=0'
                yield scrapy.Request(target_url, callback=self.find_all_app)
            try:
                url = urls[i]
            except:
                break

            url = url.replace(" ", "")
            url = url.replace("\n", "")
            yield scrapy.Request('https://cafebazaar.ir' + url, callback=self.see_app_details)
            i += 1

    def see_app_details(self, response):
        # find all details of apps
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
        try:
            dic['dev_slug'] = ''.join(response.xpath("//div[@itemprop='author']/a/@href").extract()).split('/')[-2]
        except:
            dic['dev_slug'] = self.generate_random_slug()

        category_link = ''.join(response.xpath("//span[@class='pull-right']/a/@href").extract())
        icon = ''.join(response.xpath("//img[@class='app-img']/@src").extract())
        component = response.url.split("/")[-2]

        version = version.replace("\n", "")
        version = version.strip()
        size = size.replace("\n", "")
        size = size.strip()
        act_install = act_install.replace(u"کمتر از", "").strip()
        act_install = act_install.replace(u"٬", "")
        act_install = act_install.replace(u"+", "")
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
        icon = icon.replace('\n', '')
        icon = icon.strip()

        dic['cat_name'] = category
        dic['cat_slug'] = category_link.split("/")[-2]
        dic['version'] = version if version and len(version) > 0 else "0.0"

        try:
            dic['act_install'] = int(act_install)
        except(ValueError):
            print ("kose ammat ")

        dic['size'] = int(size)
        dic['price'] = int(price)
        dic['name'] = name
        dic['dev_name'] = author
        dic['component'] = component
        dic['icon'] = icon
        dic['rate'] = rate
        # print "********************\n",dic,'\n**********************'
        yield {"status": "app", 'item': dic}

    def generate_random_slug(self, s=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(s))
