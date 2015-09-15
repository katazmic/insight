
# coding: utf-8

import json 

import pymysql as mdb

with open('CubanCigar.json') as data_file:
    data = json.load(data_file)

NumCigars = len(data.keys())

NumFeatures = len(data[data.keys()[0]].keys())



HOST = 'localhost'
USER = 'root'
PASSWD = ''
DATABASE = 'cubanCigars'



db_connect = mdb.connect(
    host = HOST,
    user = USER,
    passwd = PASSWD)


cursor = db_connect.cursor()

cursor.execute('CREATE DATABASE cigar')
cursor.execute('USE cigar')
cursor.execute("""
CREATE TABLE cigar_info(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    overall_rating TEXT,
    origin TEXT,
    link TEXT,
    appearance TEXT,
    value TEXT,
    construction TEXT,
    full_review TEXT,
    flavor TEXT,
    image TEXT,
    PRIMARY KEY (id)
    )
    """)



add_cigar = ("INSERT INTO cigar_info "
           " (name,brand,overall_rating,origin,link,appearance,value,construction,full_review,flavor,image)"
           " VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)")


cigar_info_list = ['brand','overall rating','origin','link','appearance','value','construction','full review','flavor','image']

for i in range(len(data.keys())):
    name = data.keys()[i]
    brand = str(data[name]['brand'].replace(u'\u20ac',''))
    overall_rating = str(data[name]['overall rating'].replace(u'\u20ac',''))
    origin = str(data[name]['origin'].replace(u'\u20ac',''))
    link = str(data[name]['link'].replace(u'\u20ac',''))
    appearance = str(data[name]['appearance'].replace(u'\u20ac','').replace(u'\xa0',''))
    value = str(data[name]['value'].replace(u'\u20ac',''))
    construction = str(data[name]['construction'].replace(u'\u20ac',''))
    full_review =  str(data[name]['full review'].replace(u'\xa0','').replace(u'\u20ac','').replace(u'\xe9',''))
    flavor = str(data[name]['flavor'].replace(u'\u20ac',''))
    image = str(data[name]['image'].replace(u'\u20ac',''))
    cigar_data = (name,brand,overall_rating,origin,link,appearance,value,construction,full_review,flavor,image)

    cursor.execute(add_cigar, cigar_data)
    db_connect.commit()



