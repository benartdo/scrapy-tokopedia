# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import requests


class ScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        return item


# class DuplicatesPipeline:
#     def __init__(self):
#         self.ids_seen = set()

#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         if adapter["id"] in self.ids_seen:
#             raise DropItem(f"Duplicate item found: {item!r}")
#         else:
#             self.ids_seen.add(adapter["id"])
#             return item


class PostgresDemoPipeline:
    def process_item(self, item, spider):
                        #'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
        self.connection = 'postgresql://postgres:password@localhost/scraper'

        self.cur = self.connection.cursor()

        table = """        
            CREATE TABLE IF NOT EXISTS scraper(
            name text PRIMARY KEY, 
            price text,
            image_url BYTEA,
            product_url text
        )
        """

        self.cur.execute(table)


    def process_item(self, item, spider):
        image_data = requests.get(item["image_url"]).content
        
        self.cur.execute(""" INSERT INTO scrapy (name, price, image_url, product_url) VALUES (%s,%s,%s,%s) RETURNING * """, (
            str(item["name"]),
            str(item["text"]),  
            image_data,
            str(item["product_url"])
        ))

        self.connection.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()