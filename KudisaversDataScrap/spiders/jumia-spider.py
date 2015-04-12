import scrapy
import sys

import KudisaversDataScrap.items as Items

import urlparse


class JumiaSpider(scrapy.Spider):
    name = "jumia"
    allowed_domains = ["jumia.com.ng"]
    start_urls = [
        "http://www.jumia.com.ng"
    ]

    logFile = open("./logs/jumia-log.log", "w")
    sys.stdout = logFile
    reqFile = open("./logs/jumia-requests.log", "w")
    errors = open("./logs/jumia-errors.txt", "w")

    def parse(self, response):

        sel = response.selector
        menu = sel.xpath('//div[@id="menu-header"]/ul')
