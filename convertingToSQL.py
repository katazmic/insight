
# coding: utf-8

import json 

import pymysql as mdb

with open('WhiskeyStructured.json') as data_file:
    data = json.load(data_file)

data_file.close()


HOST = 'localhost'
USER = 'root'
PASSWD = ''
DATABASE = 'WhiskeyAndCigars'



db_connect = mdb.connect(
                         host = HOST,
                         user = USER,
                         passwd = PASSWD)


cursor = db_connect.cursor()

cursor.execute('CREATE DATABASE WhiskeyAndCigars')
cursor.execute('USE WhiskeyAndCigars')

cursor.execute("""
    CREATE TABLE whiskey_info(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    link TEXT,
    full_review TEXT,
    notes TEXT,
    image TEXT,
    PRIMARY KEY (id)
    )
    """)



add_whiskey = ("INSERT INTO whiskey_info "
               " (name,link,full_review,notes,image)"
               " VALUES (%s, %s, %s, %s, %s)")


for i in range(len(data.keys())):
    name = data.keys()[i]
    link = str(data[name]['link'].replace(u'\u20ac',''))
    full_review =  str(data[name]['full review'].replace(u'\xa0','').replace(u'\u20ac','').replace(u'\xe9',''))
    notes = data[name]['notes']
    image = data[name]['image']
    whiskey_data = (name,link,full_review,notes,image)

    cursor.execute(add_whiskey, whiskey_data)





###   cigars

with open('CigarsStructured.json') as data_file:
    data = json.load(data_file)

data_file.close()

cursor.execute("""
    CREATE TABLE cigar_info(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    link TEXT,
    full_review TEXT,
    notes TEXT,
    image TEXT,
    PRIMARY KEY (id)
    )
    """)



add_whiskey = ("INSERT INTO cigar_info "
               " (name,link,full_review,notes,image)"
               " VALUES (%s, %s, %s, %s, %s)")


for i in range(len(data.keys())):
    name = data.keys()[i]
    link = str(data[name]['link'].replace(u'\u20ac',''))
    full_review =  str(data[name]['full review'].replace(u'\xa0','').replace(u'\u20ac','').replace(u'\xe9',''))
    notes = data[name]['notes']
    image = data[name]['image']
    cigar_data = (name,link,full_review,notes,image)
    
    cursor.execute(add_cigar, cigar_data)
    

    
    db_connect.commit()



