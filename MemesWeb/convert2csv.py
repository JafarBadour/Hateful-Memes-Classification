import os
from utils import progressBar
import requests, json
from shutil import copyfile

if __name__ == '__main__':
    print('getting labels')
    r = requests.get('http://18.221.173.110:5545/get_labels')
    print('done getting labels from server')
    memesdict = {}
    profiles = {}
    for line in r.content.decode().split('\n'):
        try:
            line = line.strip('\n')
            d = json.loads(line)
            dir = d['dir']
            file = d['file']

            if not d['profile'] in memesdict:
                memesdict[d['profile']] = {}

            if not f'{dir}/{file}' in memesdict[d['profile']]:
                memesdict[d['profile']][f'{dir}/{file}'] = []
            memesdict[d['profile']][f'{dir}/{file}'].append(int(d['label']))
        except:
            continue
    cnt = 0
    errs = 0
    total = sum(map(len, [memesdict[k][d] for k in memesdict.keys() for d in memesdict[k].keys()]))
    for profile_choice in memesdict.keys():
        hateful_path = 'Volunteers_data/' + profile_choice + '/hateful'
        benign = 'Volunteers_data/' + profile_choice + '/bengin'
        not_meme = 'Volunteers_data/' + profile_choice + '/not_meme'
        os.makedirs(hateful_path, exist_ok=True)
        os.makedirs(benign, exist_ok=True)
        os.makedirs(not_meme, exist_ok=True)

        for k, v in memesdict[profile_choice].items():
            meme_path = f'/home/jafar/PycharmProjects/Memes Collection/memes_images/{k}'
            if 2 in v:
                dir2copy = not_meme
            elif sum(v) * 2 > 0:

                dir2copy = hateful_path
            else:
                dir2copy = benign
            try:

                copyfile(meme_path, dir2copy + f'/{k.replace("/", "__")}')

            except Exception as e:
                print(e.args)
                errs += 1
            cnt += 1

            progressBar(token='building volunteer database', cnt=cnt, total=total)
    print(errs)
