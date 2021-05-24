from flask import Flask, make_response, render_template, request, url_for, send_file
from werkzeug.local import Local

loc = Local()

app = Flask(__name__,
            static_url_path='',
            static_folder='./static',
            template_folder='./static')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['CORS_HEADERS'] = 'Content-Type'

import os

links = list(os.walk('./memes_images'))
reslinks = []
for pardir, _, files in links:
    reslinks.extend(list(map(lambda x: pardir.replace('./memes_images/', '') + '/' + x, files)))


# return '<iframe src={0} width={1[0]} height={1[1]}></iframe>'.format(pdf, size)


@app.route('/src/<dir>/<img>/<profile>', methods=['GET'])
def get_pdf(dir, img, profile):
    import os
    print(img, '\n==========================')
    binary_img = open(f'./memes_images/{dir}/{img}', 'rb').read()
    response = make_response(binary_img)
    response.headers['Content-Type'] = 'application/img'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s' % img
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/get_links/<profile>', methods=['GET'])
def get_links(profile):
    import random
    random.shuffle(reslinks)

    labeled_reslinks = get_results(profile)
    any_labeled_links = get_results()
    reslinks_ = set(reslinks).difference(set(labeled_reslinks.keys()))
    reslinks_ = list(reslinks_)
    reslinks_.sort(key=lambda k: 7 if not k in any_labeled_links else -len(any_labeled_links[k]))
    reslinks_ = list(
        filter(lambda k: not k in any_labeled_links or len(any_labeled_links[k]) <= 5, reslinks_))
    # print(labeled_reslinks)
    reslinks_.sort(key=lambda x: -1 if 'duckduckgo' in x else 0)
    response = make_response(str(list(reslinks_)))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/classify/<dir>/<img>/<label>/<profile>', methods=['GET'])
def classify(dir, img, label, profile):
    """

    :param dir:
    :param img:
    :param label: 0 not hateful, 1 hateful
    :return:
    """
    with open('results', 'a') as f:
        import json
        f.write('\n' + json.dumps(
            {'remote_ip': request.remote_addr, 'dir': dir, 'file': img, 'label': label, 'profile': profile}))
    response = make_response('success')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/get_labels', methods=['GET'])
def get_labels():
    try:
        with open('results', 'r') as f:
            response = make_response('\n'.join(f.readlines()))
    except Exception as e:
        response = make_response('err' + e.args)

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def get_results(profile_choice=None):
    import json

    memesdict = {}
    with open('results', 'r') as f:
        for line in f.readlines():
            try:
                line = line.strip('\n')
                d = json.loads(line)
                dir = d['dir']
                file = d['file']

                if not profile_choice is None:

                    if d['profile'] != profile_choice:
                        continue
                if not f'{dir}/{file}' in memesdict:
                    memesdict[f'{dir}/{file}'] = []
                memesdict[f'{dir}/{file}'].append(int(d['label']))
            except:
                continue
    return memesdict


@app.route('/stats', methods=['GET'])
def stats():
    memesdict = get_results()
    # print(memesdict)
    hateful = 0

    for k, v in memesdict.items():
        if 2 in v:
            continue
        hateful += 1 if sum(v) * 2 >= len(v) else 0
    benign = len(memesdict) - hateful
    import matplotlib.pyplot as plt
    plt.pie([hateful, benign], explode=[0.1, 0], labels=[f'Hateful {hateful}', f'Benign {benign}'],
            colors=['red', 'blue'])

    res = f'{hateful}/{benign}'

    response = make_response(res)

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/stats/<profile>', methods=['GET'])
def stats_profile(profile):
    memesdict = get_results(profile)
    # print(memesdict)
    hateful = 0

    for k, v in memesdict.items():
        if 2 in v:
            continue
        hateful += 1 if sum(v) * 2 >= len(v) else 0
    benign = len(memesdict) - hateful
    import matplotlib.pyplot as plt
    plt.pie([hateful, benign], explode=[0.1, 0], labels=[f'Hateful {hateful}', f'Benign {benign}'],
            colors=['red', 'blue'])

    res = f'{hateful}/{benign}'

    response = make_response(res)

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=80)

"""
function server { python3 apphandler.py > /dev/null; }
function appz { python3 app.py > /dev/null; }

"""
