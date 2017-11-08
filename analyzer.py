# -*- coding: utf8 -*-

import pandas as pd

try:
    df = pd.read_pickle('analyzer.pickle')
except FileNotFoundError:
    import sqlite3
    db = sqlite3.connect('crawler.db')
    data = []
    for row in db.execute('select * from tzcs'):
        data.append(row)
    df = pd.DataFrame(
        data=data,
        columns=('id', 'name', 'sex', 'height', 'weight', 'lung', 'shortrun', 'jump', 'longrun', 'bend', 'two', 'total'))
    df.to_pickle('analyzer.pickle')
    db.close()


