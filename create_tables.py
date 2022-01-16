# -*- coding: utf-8 -*-
"""

@author: avinashvarna
"""


import datetime
import os
import io

from string import Template
from urllib.parse import urlparse
from pathlib import Path

import requests
import pandas as pd
import numpy as np
import more_itertools


def download_file(url:str, filepath:str = None):
    ''' Download file from url to specified filepath.
        If filepath is None, then the file is saved in the current directory
        and the path is returned.
    '''
    if filepath is None:
        path = urlparse(url).path
        filepath = Path(path).name
    r = requests.get(url, stream=True)
    with open(filepath, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return filepath


if __name__ == "__main__":
    _start_time = datetime.datetime.now()

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTi3Y68lIbndUd8G0BCiqcq2nD8kch9njE37aIDlEwR9tB7AbqEA5wLBKnW1kCgaNxAAVF9XwwYAC6b/pub?gid=0&single=true&output=csv"

    template = Template('''
    <h1>पदच्छेदः</h1>
    <p class='muulam text-center'>
    $text
    </p>
    <div class='padaccheda'>
    $table
    </div>
    ''')

    csv_file = download_file(url)

    SHLOKA_HTML_DIR = 'shloka'
    if not os.path.exists(SHLOKA_HTML_DIR):
        os.mkdir(SHLOKA_HTML_DIR)

    # Create HTML file for each shloka
    df = pd.read_csv(csv_file, header=None)
    shloka_starts = df[0] ==  'श्लोकः'
    shloka_starts = list(np.nonzero(shloka_starts.values)[0])
    shloka_starts.append(len(df))
    for (start, stop) in more_itertools.pairwise(shloka_starts):
        num = df.iloc[start][1]
        text = df.iloc[start][2]
        text = text.replace('।', '।<br>')
        d = df.iloc[start+2:stop]
        d.columns = df.iloc[start+1]
        s = io.StringIO()
        d.to_html(s, index=False, index_names=False,
                  classes='table table-bordered', border=0,
                  justify="center")
        table = s.getvalue()
        with open(f'{SHLOKA_HTML_DIR}/{num}.html', 'w',
                  encoding='utf8') as f:
            html = template.substitute(text=text, table=table)
            f.write(html)

    _end_time = datetime.datetime.now()
    delta = _end_time - _start_time
    print(f"Took {delta} ({delta.total_seconds()} s)")