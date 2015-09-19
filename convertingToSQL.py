
# coding: utf-8

import json 
import numpy as np
import pymysql as mdb


with open('WhiskeyStructured.json') as data_file:
    dataW = json.load(data_file)

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


for i in range(len(dataW.keys())):
    try:
        name = str(dataW.keys()[i])
        link = str(dataW[name]['link'])
        notes = str(dataW[name]['notes'])
        palate = str(dataW[name]['Palate'])
        nose = str(dataW[name]['Nose'])
        categories = str(dataW[name]['categories'])
        image = str(dataW[name]['image'])
        whiskey_data = (name,link,palate,nose,notes,categories,image)
        cursor.execute(add_whiskey, whiskey_data)
        db_connect.commit()
    except:
        print name


###   cigars

with open('CigarStructured.json') as data_file:
    dataC = json.load(data_file)

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


for i in range(len(dataC.keys())):
    try:
        name = str(dataC.keys()[i])
        link = str(dataC[name]['link'])
        notes = str(dataC[name]['notes'])
        flavor = str(dataC[name]['flavor'])
        categories = str(dataC[name]['categories'])
        image = str(dataC[name]['image'])
        cigar_data = (name,link,flavor,notes,categories,image)
        cursor.execute(add_cigar, cigar_data)
        db_connect.commit()
    except:
        print name



################# MATCHING TABLE


cursor.execute("""
    DROP TABLE cigar_whiskey_match
    """)

cursor.execute("""
    CREATE TABLE cigar_whiskey_match(
    id INTEGER NOT NULL AUTO_INCREMENT,
    whiskeyName TEXT NOT NULL,
    cigarName TEXT NOT NULL,
    matchScore TEXT,
    PRIMARY KEY (id)
    )
    """)

add_match = ("INSERT INTO cigar_whiskey_match "
             " (whiskeyName,cigarName,matchScore)"
             " VALUES (%s, %s, %s)")

data_matched = []

for w in dataW:
    whiskey = dataW[w]
    wL = np.sqrt(float(np.dot(whiskey['binaryNotes'],whiskey['binaryNotes'])))
    for c in dataC:
        cigar = dataC[c]
        cL = np.sqrt(float(np.dot(cigar['binaryNotes'],cigar['binaryNotes'])))
        scr = float(np.dot(dataW[w]['binaryNotes'],dataC[c]['binaryNotes']))/(float(wL)*float(cL))
        data_matched.append(dict(whiskeyName = whiskey['name'], cigarName = cigar['name'], matchScore = scr))    



k=0
for matched in data_matched:
    match_data = (matched['whiskeyName'],matched['cigarName'], matched['matchScore'])
    bla = cursor.execute(add_match, match_data)
    print k 
    db_connect.commit()
    k=k+1



###################################

