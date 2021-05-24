# import scrapy
# from memes.queries import get_queries
# from memes.pipelines import Flagger
#
#
#
# class RedditSpider(scrapy.Spider):
#     name = 'reddit'
#     #allowed_domains = ['reddit']
#     start_urls = ['https://www.reddit.com/r/memes/']+list(
#         map(lambda x: f'https://www.reddit.com/search/?q={x}+meme', get_queries()))
#     Flagger().write_info(name)
#
#     def parse(self, response):
#         raw_image_urls = response.css('img::attr(src)').getall()
#
#         raw_image_urls = list(map(response.urljoin, raw_image_urls))
#         yield {
#             'image_urls': raw_image_urls
#         }
#
#         crawl_links = list(map(response.urljoin, response.css('a::attr(href)').getall()))
#         #yield {'crawl_links' : crawl_links}
#         for link in crawl_links:
#             yield scrapy.Request(link, callback=self.parse)