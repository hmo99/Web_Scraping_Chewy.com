# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ChewyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    #Product Info
    
    productName = scrapy.Field() #individual rating, need to calculate individual rate by myself
    brandName = scrapy.Field()
    price = scrapy.Field()
    num_of_reviews = scrapy.Field()
    date=scrapy.Field()
    reviewRating=scrapy.Field()
    reviewTitle=scrapy.Field()
    reviewContent=scrapy.Field()
    percentRec=scrapy.Field()