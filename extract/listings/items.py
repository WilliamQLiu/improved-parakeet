# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ListingsItem(scrapy.Item):
    """
    Parse an individual listing for the following:
        Location - StreetAddress
        ListingDetails - Price, MlsId, MlsName, DateListed
        RentalDetails - 
        BasicDetails - Description, Bathrooms
        RichDetails - Appliances
    """
    mls_id = scrapy.Field()
    mls_name = scrapy.Field()
    mls_date_listed = scrapy.Field()
    street_address = scrapy.Field()
    price = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms_full = scrapy.Field()
    bathrooms_half = scrapy.Field()
    appliances = scrapy.Field()
    rooms = scrapy.Field()
    description = scrapy.Field()
