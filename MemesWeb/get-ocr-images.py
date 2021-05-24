import json
import os
import time
from datetime import datetime
import sys
import pandas as pd
from utils import progressBar, write_on_line, change_ip
from threading import Thread
from datetime import datetime as dt


def log(message: str):
    date = datetime.strftime(datetime.utcnow(), 'UTC: %d.%m.%Y')
    d = {
        'date': date,
        'time': datetime.strftime(datetime.utcnow(), '%H.%Mm.%Ss.%fms'),
        'log': message
    }
    with open('ErrorLog', 'a') as f:
        f.write(json.dumps(d) + '\n')


api_keys = ['fe56ef020088957', 'd20b9939cf88957', '06aaf1f28c88957', '059de453fd88957', '637c76083088957',
            '45c9ed799988957', '11b22818b388957', '190588abcc88957', 'ca09953b7a88957'
    , 'df4cc8910f88957', '9495403da388957', '38766f6eb488957', 'cd87db984588957', 'c26afaf22388957', '9441fc802788957',
            'b11b55d31d88957', 'b02f6fdcb588957', '2e1238f24b88957', 'c26b86d5ae88957', '366dba276388957',
            '24ca3c04bc88957', '371e898b6288957', 'ffef10a6c788957', 'bdf14e381088957', '9c45e406cb88957',
            '55979407e488957']


# """
# curl --location --request POST 'https://api.ocr.space/parse/image' \
# --header 'apikey: helloworld' \
# --form 'language="eng"' \
# --form 'isOverlayRequired="false"' \
# --form 'url="http://dl.a9t9.com/ocrbenchmark/eng.png"' \
# --form 'iscreatesearchablepdf="false"' \
# --form 'issearchablepdfhidetextlayer="false""""


class Worker(Thread):

    def __init__(self, link, api_key, threadID):
        Thread.__init__(self)
        self.link = link
        self.api_key = api_key
        self.threadID = threadID
        self.result = None
        self.cnt = 0
        self.error = False

    def run(self):
        # self.params = list(map(lambda x: x.drop(['Unnamed: 0'], axis=1), self.params))
        link = self.link

        img_url = f'http://18.221.173.110:5545/src/{link}/nobody'
        import os

        filename, file_extension = os.path.splitext(link)
        file_extension = file_extension.replace('.', '')
        if len(file_extension) == 0:
            file_extension = 'jpeg'
        dir, filename = filename.split('/')
        dir = dir.replace(' ', '')
        os.makedirs(f'./OCR-Dump/{dir}', exist_ok=True)
        # print(filename, file_extension, dir)
        # print(img_url)
        # # print(img_url)
        # r = requests.get(img_url)
        # open(f'download.{file_extension}','wb').write(r.content)

        if os.path.isfile(f'./OCR-Dump/{dir}/{filename}.json'):
            return

        r = requests.post(url, data={
            'apikey': self.api_key,
            'language': 'eng',
            'isOverlayRequired': 'true',
            'url': img_url,
            'iscreatesearchablepdf': 'false',
            'issearchablepdfhidetextlayer': 'false',
            'filetype': file_extension
        })
        import time

        # print(r.content)

        with open(f'./OCR-Dump/{dir}/{filename}.json', 'wb') as f:
            f.write(r.content)
            f.close()

        with open(f'./OCR-Dump/{dir}/{filename}.json', 'r') as f:
            import json

            try:
                d = json.load(f)
                assert d['OCRExitCode'] == 1

            except Exception as e:
                print(self.threadID, ' thread id')
                print(e.args)
                print(r.content)
                self.error = True
                os.remove(f'./OCR-Dump/{dir}/{filename}.json')


if __name__ == '__main__':
    import requests
    import sys

    # change_ip()
    write_on_line('Getting data from server')

    url = 'https://api.ocr.space/parse/image'
    links = requests.get('http://18.221.173.110:5545/get_links/nobody').content
    links = links.decode()
    links = links.split(',')
    links = list(map(lambda x: x.strip('[\'\']').replace("\'", '').replace(' ', ''), links))
    requests_number = 0
    api_index = 0
    for i in range(6130, 25000):
        workers = []

        progressBar(
            token=f'Processing images jsons {i}/{25000}',
            cnt=i,
            total=25000
        )

        filename, file_extension = os.path.splitext(links[i])
        file_extension = file_extension.replace('.', '')
        if len(file_extension) == 0:
            file_extension = 'jpeg'

        dir, filename = filename.split('/')
        if os.path.isfile(f'./OCR-Dump/{dir}/{filename}.json'):
            continue
        requests_number += 1
        workers.append(
            Worker(
                link=links[i],
                api_key=api_keys[api_index],
                threadID=i % 25
            )
        )

        for w in workers:
            w.start()
        for w in workers:
            w.join()
        if requests_number == 180 or any(w.error for w in workers):
            requests_number = 0
            api_index = (api_index + 1) % len(api_keys)

            change_ip()
        time.sleep(1)
        # if (i // 25) % 20 == 0:
        #     change_ip()
