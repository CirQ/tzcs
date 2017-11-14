# -*- coding: utf8 -*-

import pandas as pd

# The data preprocessing's logic is:
# when cleaning data, I drop those data that disobey all thresholds;
# when using data, I drop the data the disobey at least one threshold.

min_thr = {
    'height': 100.0,
    'weight': 30.0,
    'lung': 1,
    'shortrun': 5.0,
    'jump': 50.0,
    'longrun': 2.20,
    'bend': -20.0,
    'two': 0
}

max_thr = {
    'height': 200.0,
    'weight': 150.0,
    'lung': 10000,
    'shortrun': 20.0,
    'jump': 320.0,
    'longrun': 50.0,
    'bend': 50.0,
    'two': 100
}

def opener():
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
        before, after, df = clean(df)
        # print('Before size: %d;  After size: %d.' % (before, after))  # before 23810  after 20174
        df.to_pickle('analyzer.pickle')
        db.close()
    return df

def clean(df):
    before_size = df.shape[0]
    df = df[
        ((df['height'] > min_thr['height']) & (df['height'] < max_thr['height'])) |
        ((df['weight'] > min_thr['weight']) & (df['weight'] < max_thr['weight'])) |
        ((df['lung'] > min_thr['lung']) & (df['lung'] < max_thr['lung'])) |
        ((df['shortrun'] > min_thr['shortrun']) & (df['shortrun'] < max_thr['shortrun'])) |
        ((df['jump'] > min_thr['jump']) & (df['jump'] < max_thr['jump'])) |
        ((df['longrun'] > min_thr['longrun']) & (df['longrun'] < max_thr['longrun'])) |
        ((df['bend'] > min_thr['bend']) & (df['bend'] < max_thr['bend'])) |
        ((df['two'] > min_thr['two']) & (df['two'] < max_thr['two'])) ]
    after_size = df.shape[0]
    return before_size, after_size, df

def max_min(df):
    print(df.describe())
    pass


if __name__ == '__main__':
    dataframe = opener()
    max_min(dataframe)
