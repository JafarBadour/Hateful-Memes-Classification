import json
import os
import time
from datetime import datetime
import sys

def log(message: str):
    date = datetime.strftime(datetime.utcnow(), 'UTC: %d.%m.%Y')
    d = {
        'date': date,
        'time': datetime.strftime(datetime.utcnow(), '%H.%Mm.%Ss.%fms'),
        'log': message
    }
    with open('ErrorLog', 'a') as f:
        f.write(json.dumps(d) + '\n')
def write_on_line(text):
    sys.stdout.write(f'\r{text}')
    sys.stdout.flush()

def progressBar(token, cnt, total, barLength=20):
    import sys
    percent = float(cnt) * 100 / total
    arrow = '-' * int(percent / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\r%s: Progress: [%s%s] %f %% ' % (
        token, arrow, spaces, percent))
    sys.stdout.flush()

def whats_my_ip():
    import requests
    """Return current ip address."""
    try:
        data = json.loads(requests.get("http://ip.jsontest.com/").content)
    except:
        return 'Error in jcontest'
    return data["ip"]


def change_ip():
    import random
    import subprocess
    oldip = whats_my_ip()
    countries = ['uk', 'france', 'germany', 'us', 'italy', 'portugal', 'canada', 'norway']

    bash_command = f'echo bakhetle | sudo -S nordvpn connect {countries[random.randint(0, 6)]}'
    # 'Put your credentials in a normal terminal instance {errlogin, password} then run this'
    process = subprocess.Popen(
        bash_command,
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.wait()
    newip = whats_my_ip()
    time.sleep(2)
    print('ip changed successfully, you hacked them soldier!!', 'Thread Scheduler')
    print(f'{oldip} ==> {newip}', 'Thread Scheduler')