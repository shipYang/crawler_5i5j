# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    title=scrapy.Field()
    housing_estate=scrapy.Field()
    floor=scrapy.Field()
    price_num=scrapy.Field()
    rooms=scrapy.Field()
    floorage=scrapy.Field()
    orientation=scrapy.Field()
    decoration_situation=scrapy.Field()
    year=scrapy.Field()
    address=scrapy.Field()
    house_code=scrapy.Field()
    price_unit_num=scrapy.Field()
    term = scrapy.Field()






