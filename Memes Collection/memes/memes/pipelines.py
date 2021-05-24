# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import mimetypes
import os

from imapclient.util import to_bytes
from scrapy.pipelines.images import ImagesPipeline
from twisted.web.http import urlparse


class Flagger:
    def __init__(self):
        self.ran = False
        self.information = {}

    def info(self):
        return self.information

    def set_info(self):
        self.information = open('current_domain', 'r').readlines()[0]

    def write_info(self, x):
        print('WRITING ++++++ ', x)
        print('WRITING ++++++ ', x)
        open('current_domain', 'w').write(x)


class CostumedPipeLine(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        try:
            self.flagger.info()
        except:
            self.flagger = Flagger()
            self.flagger.set_info()

        media_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        media_ext = os.path.splitext(request.url)[1]
        # Handles empty and wild extensions by trying to guess the
        # mime type then extension or default to empty string otherwise
        if media_ext not in mimetypes.types_map:
            media_ext = ''
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        url = request.url
        # try:
        #     domain = urlparse(url.encode('utf-8')).netloc.decode()
        # except Exception as e:
        #     print('^^^^^^^^^^')
        #     print(e.args)
        #     assert 0
        # while domain.count('.') > 2:
        #     domain = domain[domain.find('.') + 1:]
        # if domain.count('.') == 1:
        #     st = domain.find('.')
        #     domain = domain[:st]
        #
        # if domain.count('.') == 2:
        #     st = domain.find('.')
        #     domain = domain[st + 1:domain[st + 1:].find('.') + st + 1]
        domain = self.flagger.info()

        print('writing successful &&&&&&&&&', domain)
        return f'{domain}/{media_guid}{media_ext}'
