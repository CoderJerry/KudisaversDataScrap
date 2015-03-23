# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.contrib.djangoitem import DjangoItem



class KudisaversdatascrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class item_computers(scrapy.Item):
    sectionName = scrapy.Field()
    catName = scrapy.Field()
    catUrl = scrapy.Field()
    prodTypeName = scrapy.Field()
    prodTypeUrl = scrapy.Field()
    prodName = scrapy.Field()
    prodUrl = scrapy.Field()
    prodDesc = scrapy.Field()
    prodProperties  =scrapy.Field()
    reviews = scrapy.Field()
    imageLink = scrapy.Field()
    offerPrice = scrapy.Field()
    availability = scrapy.Field()


class KudisaversItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SectionItem(scrapy.Item):
    name = scrapy.Field()


class ProductItem(scrapy.Item):
    site = scrapy.Field()
    section = scrapy.Field()
    category = scrapy.Field()
    prodType = scrapy.Field()
    brand = scrapy.Field()
    prodName = scrapy.Field()
    prodUrl = scrapy.Field()
    prodDesc = scrapy.Field()
    prodProperties  =scrapy.Field()
    reviews = scrapy.Field()
    imageLink = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    availability = scrapy.Field()
