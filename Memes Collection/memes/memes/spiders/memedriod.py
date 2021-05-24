import scrapy
from memes.queries import get_queries
from memes.pipelines import Flagger
import time

class MemedriodSpider(scrapy.Spider):
    name = 'memedriod'
    allowed_domains = ['memedroid.com']
    start_urls =  list(
        map(lambda x: f'https://www.memedroid.com/search?query={x}', get_queries()))
    print("Changing domain to ", name)
    Flagger().write_info(name)



    def parse(self, response):
        raw_image_urls = response.css('.img-responsive::attr(src)').getall()

        raw_image_urls = list(map(response.urljoin, raw_image_urls))
        yield {
            'image_urls': raw_image_urls
        }

        crawl_links = list(map(response.urljoin, response.css('a::attr(href)').getall()))
        for link in crawl_links:
            yield scrapy.Request(link, callback=self.parse)
