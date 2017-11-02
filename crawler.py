# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
from requests import Session
import re
import sqlite3
import logging
import logging.handlers

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(name)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='tzcs.log',
    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(filename)-10s:%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('tzcs').addHandler(console)
logger = logging.getLogger('tzcs')

db = sqlite3.connect('crawler.db')
cur = db.cursor()
try:
    db.execute('''CREATE TABLE tzcs(
            id          INT PRIMARY KEY NOT NULL,
            name        TEXT            NOT NULL,
            sex         TEXT            NOT NULL,
            height      REAL,
            weight      REAL,
            lung        INTEGER,
            shortrun    REAL,
            jump        REAL,
            longrun     REAL,
            bend        REAL,
            two         INTEGER,
            total       INTEGER
            );''')
    db.commit()
except sqlite3.OperationalError:
    pass
db.text_factory = str

insert_sql = 'INSERT INTO tzcs (id, name, sex, height, weight, lung, shortrun, jump, longrun, bend, two, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'

s = Session()
s.cookies.set('JSESSIONID', '')
url = 'https://tzcs.jnu.edu.cn/SportWeb/health_info/listdetalhistroyScore.jsp?studentNo={}&gradeNo={}'

infore = re.compile(r'^学号:(\d+?)(?:\xe3\x80\x80){3}姓名：([\S\s]+?)(?:\xe3\x80\x80){3}性别：(\S+?)$')

try:
    for i in range(1, 10000):
        stuid = 2016050000 + i
        purl = url.format(stuid, 1)
        resp = s.get(purl, allow_redirects=False)
        if(resp.status_code == 200):
            bs = BeautifulSoup(s.get(purl).text, 'lxml')
            table = bs.find('table', cellspacing='1')
            rows = table.find_all('tr')
            info = rows[1].td.string.strip().encode('utf8')
            num, name, sex = infore.match(info).groups()
            num = int(num)
            height = float(rows[3].find_all('td')[2].string.strip())
            weight = float(rows[4].find_all('td')[2].string.strip())
            lung = int(rows[5].find_all('td')[2].string.strip())
            shortrun = float(rows[6].find_all('td')[2].string.strip())
            jump = float(rows[7].find_all('td')[2].string.strip())
            longrun = float(rows[8].find_all('td')[2].string.strip())
            bend = float(rows[9].find_all('td')[2].string.strip())
            two = int(rows[10].find_all('td')[2].string.strip())
            total = int(rows[13].find_all('th')[3].string.strip())
            cur.execute(insert_sql,
                    (num, name, sex, height, weight, lung, shortrun, jump, longrun, bend, two, total))
            logger.info('[SUCCESS] dumped data for id: %d', stuid)
        else:
            logger.warning('[FAILED] error for id: %d', stuid)
except KeyboardInterrupt:
    pass
finally:
    db.commit()
    cur.close()
    db.close()
