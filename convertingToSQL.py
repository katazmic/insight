
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



