# -*- coding: utf8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
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

def clean(df: pd.DataFrame):
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

def split_sex(df: pd.DataFrame):
    return df[df['sex']=='男'], df[df['sex']=='女']

def max_min(df, ret=False):
    h, w, l, sr, j, lr, b, t = df['height'], df['weight'], df['lung'], df['shortrun'], df['jump'], df['longrun'], df['bend'], df['two']
    height = h[(h > min_thr['height']) & (h < max_thr['height'])].describe(percentiles=[])
    weight = w[(w > min_thr['weight']) & (w < max_thr['weight'])].describe(percentiles=[])
    lung = l[(l > min_thr['lung']) & (l < max_thr['lung'])].describe(percentiles=[])
    shortrun = sr[(sr > min_thr['shortrun']) & (sr < max_thr['shortrun'])].describe(percentiles=[])
    jump = j[(j > min_thr['jump']) & (j < max_thr['jump'])].describe(percentiles=[])
    longrun = lr[(lr > min_thr['longrun']) & (lr < max_thr['longrun'])].describe(percentiles=[])
    bend = b[(b > min_thr['bend']) & (b < max_thr['bend'])].describe(percentiles=[])
    two = t[(t > min_thr['two']) & (t < max_thr['two'])].describe(percentiles=[])
    stat = pd.DataFrame([height, weight, lung, shortrun, jump, longrun, bend, two])
    if ret:
        return stat
    else:
        print(stat)

def filter_column(df, col):
    return df[(df[col] > min_thr[col]) & (df[col] < max_thr[col])][col]

def male_female_distribution_compare(mdf, fdf, col):
    mseries = filter_column(mdf, col)
    fseries = filter_column(fdf, col)
    label = 'The Distribution of %s for Male' % col.capitalize()
    sns.set_style('darkgrid', {'axes.facecolor':'0.9'})
    plt.subplots(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.xlim(min_thr[col], max_thr[col])
    sns.distplot(mseries, axlabel=label)
    plt.subplot(2, 1, 2)
    plt.xlim(min_thr[col], max_thr[col])
    sns.distplot(fseries, axlabel=label)
    plt.show()

def draw_distribution(df, sex, col):
    series = filter_column(df, col)
    label = 'The Distribution of %s for %s' % (series.name.capitalize(), sex.capitalize())
    sns.set_style('darkgrid', {'axes.facecolor':'0.9'})
    sns.distplot(series, axlabel=label)
    plt.show()



if __name__ == '__main__':
    dataframe = opener()
    maleframe, femaleframe = split_sex(dataframe)
    male_female_distribution_compare(maleframe, femaleframe, 'longrun')
    # draw_distribution(maleframe, 'male', 'height')
