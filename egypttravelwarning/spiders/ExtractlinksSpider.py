# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

from egypttravelwarning.items import TravelWarningItem
import dateparser



class ExtractlinksSpider(scrapy.Spider):
    name = "extractLinks"
    allowed_domains = ["eg.usembassy.gov"]
    base_url = 'https://eg.usembassy.gov/u-s-citizen-services/security-and-travel-information/'
    start_urls = [base_url]

    def parse(self, response):
        links = Selector(response).xpath('//div[@class="mo-page-content"]/ul/li/a[@class="travelalertbordernone"]')

        for link in links:
            item = TravelWarningItem()
            item['url'] = link.xpath('@href').extract()[0]
            title = str(link.xpath('./text()').extract()[0])
            item['title'] = title
            item['date'] = dateparser.parse(title[title.index('(')+1:-1])

            yield item


    def errback(self, response):
        pass


def notThreadSafe(x):
    """do something that isn't thread-safe"""
    pass


configure_logging()
project_settings = get_project_settings()

runner = CrawlerProcess(settings=project_settings)


@defer.inlineCallbacks
def crawl():
    #yield runner.crawl(ExtractlinksSpider)
    yield runner.crawl(ExtractlinksSpider)
    reactor.stop()


try:
    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished
except:
    pass
