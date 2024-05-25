# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

# def serialize_price(value):
#     return f'Rp. {str(value)}'

class TokopediaItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()

