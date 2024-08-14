import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from urllib.parse import urljoin
from scraper.items import TokopediaItem

class tokopediaSearch(scrapy.Spider):
    name = 'tokopedia-search'
    # allowed_domains = ['tokopedia.com']
    # start_urls = ['https://www.tokopedia.com/search?navsource=&page=1&q=buku']


    def start_requests(self):
        keyword_list = 'buku'
        #page
        for i in range(1, 5):
            input_url = f'https://www.tokopedia.com/search?navsource=&page={i}&q={keyword_list}'
            yield scrapy.Request(url=input_url, callback=self.parse_search_results, 
                                meta={'keyword': keyword_list,
                                       "playwright": True, 
                                       "playwright_include_page": True,
                                       "playwright_page_methods": [ PageMethod('wait_for_selector', 'div.css-5wh65g') ]
                                    },
                                errback=self.errback_close_page
                                )  
    
    async def parse_search_results(self, response):
            keyword= response.meta['keyword']
            page = response.meta["playwright_page"]

            for i in range(1, 3):
                scroll_count = 5 * i
                    
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            await page.wait_for_selector(f'div.css-5wh65g:nth-child({scroll_count})')
            await page.wait_for_timeout(2000)

            html = await page.content()
            await page.close()
            response_scroll = Selector(text=html)

            self.logger.info(f"Mencari hasil untuk: {keyword}")
            
            # search_products = response_scroll.css("div.css-5wh65g")
            name_links = response_scroll.xpath('//div[contains(@class, "css-5wh65g")]//div[contains(@class, "VKNwBTYQmj8+cxNrCQBD6g==")]//span/text()')
            price_links = response_scroll.xpath('//div[contains(@class, "css-5wh65g")]//div[contains(@class, "_8cR53N0JqdRc+mQCckhS0g==")]/text()')
            image_links =  response_scroll.xpath('//div[contains(@class, "css-5wh65g")]//div/div/div/img[contains(@class, "css-1c345mg N8xmpVrww3v8HjDVw7D5rg==")]/@src')
            product_links = response_scroll.xpath('//div[contains(@class, "css-5wh65g")]//a/@href')
            
            for name, price, image, link in zip(name_links, price_links, image_links, product_links):
                self.logger.info("Processing product")
                
                relative_url = link.get()
                product_url = urljoin('https://www.tokopedia.com/', relative_url)
                name = name.get()
                price = price.get()
                image_url = image.get()
                
                item = TokopediaItem()
                item['name'] = name
                item['price'] = price
                item['image_url'] = image_url
                item['product_url'] = product_url
                yield item

    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        await page.context.close()