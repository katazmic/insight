
# coding: utf-8

import json 
import numpy as np
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
    DROP TABLE whiskey_info
    """)

cursor.execute("""
    CREATE TABLE whiskey_info(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    link TEXT,
    palate TEXT,
    nose TEXT,
    notes TEXT,
    categories TEXT,
    image TEXT,
    PRIMARY KEY (id)
    )
    """)


add_whiskey = ("INSERT INTO whiskey_info "
               " (name,link,palate,nose,notes,categories,image)"
               " VALUES (%s, %s, %s, %s, %s, %s,%s)")


for i in range(len(data.keys())):
    try:
        name = str(data.keys()[i])
        link = str(data[name]['link'])
        notes = str(data[name]['notes'])
        palate = str(data[name]['Palate'])
        nose = str(data[name]['Nose'])
        categories = str(data[name]['categories'])
        image = str(data[name]['image'])
        whiskey_data = (name,link,palate,nose,notes,categories,image)
        cursor.execute(add_whiskey, whiskey_data)
        db_connect.commit()
    except:
        print name


###   cigars

with open('CigarStructured.json') as data_file:
    data = json.load(data_file)

data_file.close()


cursor.execute("""
    DROP TABLE cigar_info
    """)

cursor.execute("""
    CREATE TABLE cigar_info(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    link TEXT,
    flavor TEXT,
    notes TEXT,
    categories TEXT,
    image TEXT,
    PRIMARY KEY (id)
    )
    """)

add_cigar = ("INSERT INTO cigar_info "
               " (name,link,flavor,notes,categories,image)"
               " VALUES (%s, %s, %s, %s, %s,%s)")


for i in range(len(data.keys())):
    try:
        name = str(data.keys()[i])
        link = str(data[name]['link'])
        notes = str(data[name]['notes'])
        flavor = str(data[name]['flavor'])
        categories = str(data[name]['categories'])
        image = str(data[name]['image'])
        cigar_data = (name,link,flavor,notes,categories,image)
        cursor.execute(add_cigar, cigar_data)
        db_connect.commit()
    except:
        print name


with open('CigarStructured.json') as data_file:
    dataC = json.load(data_file)

data_file.close()

with open('WhiskeyStructured.json') as data_file:
    dataW = json.load(data_file)

data_file.close()

data_matched = []

for w in dataW.keys():
    whName = str(w)
    wL = np.dot(dataW[w]['binaryCategories'],dataW[w]['binaryCategories'])
    for c in dataC.keys():
        cL = np.dot(dataC[c]['binaryCategories'],dataC[c]['binaryCategories'])
        crName = str(c)
        scr = float(np.dot(dataW[w]['binaryCategories'],dataC[c]['binaryCategories']))/(float(wL)*float(cL))
        data_matched.append(dict(whiskeyName = whName, cigarName = crName, matchScore = scr))
    


cursor.execute("""
    DROP TABLE cigar_whiskey_match
    """)

cursor.execute("""
    CREATE TABLE cigar_whiskey_match(
    id INTEGER NOT NULL AUTO_INCREMENT,
    whiskeyName TEXT NOT NULL,
    cigarName TEXT NOT NULL,
    matchScore FLOAT,
    PRIMARY KEY (id)
    )
    """)

add_match = ("INSERT INTO cigar_whiskey_match "
             " (whiskeyName,cigarName,matchScore)"
             " VALUES (%s, %s, %f)")


for matched in data_matched:
    match_data = (matched['whiskeyName'],matched['cigarName'], matched['matchScore'])
    print type(match_data['matxhScore'])
    cursor.execute(add_match, match_data)
    db_connect.commit()
    



