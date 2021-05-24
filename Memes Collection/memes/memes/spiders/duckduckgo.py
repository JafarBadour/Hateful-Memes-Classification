# import scrapy
#
# from memes.queries import get_queries
# from memes.pipelines import Flagger
#
# import requests
# import re
# import json
# import os
#
#
# def duckduckgo_search(keywords, max_results=None):
#     url = 'https://duckduckgo.com/'
#     params = {
#         'q': keywords
#     }
#     res = requests.post(url, data=params)
#     searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)
#
#     if not searchObj:
#         print("Token Parsing Failed !")
#         return -1
#
#     headers = {
#         'dnt': '1',
#         'accept-encoding': 'gzip, deflate, sdch, br',
#         'x-requested-with': 'XMLHttpRequest',
#         'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6,ms;q=0.4',
#         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#         'accept': 'application/json, text/javascript, */*; q=0.01',
#         'referer': 'https://duckduckgo.com/',
#         'authority': 'duckduckgo.com',
#     }
#
#
#
#     requestUrl = url + "i.js"
#
#     try:
#         images = []
#         for p in range(10):
#             params = (
#                 ('l', 'wt-wt'),
#                 ('o', 'json'),
#                 ('q', keywords),
#                 ('vqd', searchObj.group(1)),
#                 ('f', ',,,'),
#                 ('p', str(p))
#             )
#             res = requests.get(requestUrl, headers=headers, params=params)
#
#             data = json.loads(res.text)
#             print('%%%%%%% len=', len(data['results']))
#             images.extend(list(map(lambda x: x['image'], data['results'])))
#         return images
#     except ValueError as e:
#         print('Please try later.')
#
#     # logger.debug("Hitting Url Success : %s", requestUrl)
#
# class DuckduckgoSpider(scrapy.Spider):
#     name = 'duckduckgo'
#     #allowed_domains = ['duckduckgo.com/']
#     start_urls = list(
#         map(lambda x: f'https://duckduckgo.com/?q={x}+meme&iax=images&ia=images', get_queries()))
#     Flagger().write_info(name)
#     def parse(self, response):
#
#         #raw_image_urls = response.css('.tile--img__img::attr(src)').getall()
#         s = (response.url.replace('https://duckduckgo.com/?q=',''))
#         s = s[:s.find('&')]
#         #raw_image_urls =duckduckgo_search('')
#         image_urls = duckduckgo_search(s)
#         # print(image_urls)
#         # image_urls = []
#         print(image_urls)
#         yield {
#             'image_urls': image_urls
#         }
