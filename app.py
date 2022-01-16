# -*- coding: utf-8 -*-
"""

@author: avinashvarna
"""


import os

from glob import glob
from natsort import natsorted
from base64 import b64encode
from flask import Flask, url_for, render_template


app = Flask(__name__)

app.config.update(
  DEBUG=True,
  # Used to encrypt session cookies.
  SECRET_KEY=b64encode(os.urandom(24)).decode('utf-8'),
)

SHLOKA_HTML_DIR = 'shloka'

files = glob(f'{SHLOKA_HTML_DIR}/*.html')
files = natsorted(files)
shlokas = [os.path.splitext(os.path.basename(f))[0] for f in files]
shloka_idx = {f: i for i, f in enumerate(shlokas)}


@app.route('/shloka/<string:shloka_num>/')
def shloka(shloka_num):
    filename = f'{SHLOKA_HTML_DIR}/{shloka_num}.html'
    if os.path.exists(filename):
        with open(filename, encoding='utf8') as f:
            table = f.read()
        data = {}
        data['title'] = f'अमरकोषः -  {shloka_num}'
        data['table'] = table
        idx = shloka_idx[shloka_num]
        if idx > 0:
            # Prev shloka
            prev = shlokas[idx-1]
            data['prev'] = url_for('shloka', shloka_num=prev)
        if idx < (len(shlokas)-1):
            # Next shloka
            next_shloka = shlokas[idx+1]
            data['next'] = url_for('shloka', shloka_num=next_shloka)

        return render_template('shloka.html', data=data)


@app.route('/')
def index():
    data = {}
    data['title'] = 'श्लोकाः'
    data['shlokas'] = shlokas
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
