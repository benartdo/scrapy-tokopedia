import scrapy
from urllib.parse import urljoin
from scraper.items import TokopediaItem
import random

class tokopediaSearch(scrapy.Spider):
    name = 'tokopedia-search'
    # allowed_domains = ['tokopedia.com']
    # start_urls = ['https://www.tokopedia.com/search?navsource=&page=1&q=buku']


    def start_requests(self):
        keyword_list = ['buku']
        for key in keyword_list:
            for i in range(1, 10):
                input_url = f'https://www.tokopedia.com/search?navsource=&page={i}&q={key}'
                yield scrapy.Request(url=input_url, callback=self.parse_search_results, meta={'keyword': key})
    
    def parse_search_results(self, response):
            keyword = response.meta['keyword']
            self.logger.info(f"Mencari hasil untuk: {keyword}")

            search_products = response.css("div.css-19oqosi")
            prices = response.css("div.css-1asz3by")
            for product, price in zip(search_products, prices):
                self.logger.info("Processing product")
                relative_url = product.css("a::attr(href)").get()
                if relative_url:
                    product_url = urljoin('https://www.tokopedia.com/', relative_url)
                    name = product.css("img.css-1q90pod::attr(alt)").get()
                    price = price.css(".prd_link-product-price::text").get()
                    image_url = product.css("img.css-1q90pod::attr(src)").get()
                    
                    item = TokopediaItem()
                    item['name'] = name
                    item['price'] = price
                    item['image_url'] = image_url
                    item['product_url'] = product_url
                    yield item
