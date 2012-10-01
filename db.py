#!/usr/bin/env python
#-*- encode:utf-8 -*-

import sqlite3

db_name = None
db = None
cursor = None

def connect():
    global db, cursor
    db = sqlite3.connect("testing.db")
    cursor = db.cursor()

def init_table():
    global cursor
    query = (
        'CREATE TABLE IF NOT EXISTS "{}" ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'artis TEXT(10) NOT NULL,'
            'judul TEXT NOT NULL,'
            'lirik TEXT NOT NULL'
    ')').format("lirik_tb")
    cursor.execute(query)

def add_data(artis, judul, lirik):
    global cursor
    query = (
        'INSERT INTO "{}" (artis, judul, lirik) '
        'values ("{}", "{}", "{}")'
    ).format("lirik_tb", str(artis), str(judul), str(lirik))
    cursor.execute(query)

def get_data(judul):
    global cursor
    query = (
        'SELECT artis,judul,lirik FROM lirik_tb '
        'WHERE judul == "{}"'
    ).format(judul)
    cursor.execute(query)
    return iter(cursor)

def get_all_data():
    global cursor
    query = (
        "SELECT artis,judul FROM lirik_tb ORDER BY id DESC"
    )
    cursor.execute(query)
    return iter(cursor)

def close_all():
    global db, cursor
    cursor.close()
    db.close()

def commit():
    global db
    db.commit()

def begin():
    global db
    db.execute("BEGIN TRANSACTION")

def drop_table():
    global cursor
    cursor.execute("DROP TABLE IF EXISTS lirik_tb")

def rollback():
    global db
    db.rollback()

def update(col_name, data_new, where_):
    global cursor
    query = (
        'UPDATE lirik_tb'
        ' SET "{}" = "{}"'
        ' WHERE judul == "{}"'
    ).format(col_name, data_new, where_)
    cursor.execute(query)
    commit()
    # XXX: Testing only
    for i in iter(cursor):
        print i

if __name__ == "__main__":
    connect()
    #drop_table()
    init_table()
    #begin()
    add_data("Noah", "Separuh aku", "Nananananananana.............")
    add_data("Peterpan", "Ada apa denganmu", "Nanasmndmanf,afnamsnf...........")
    add_data("Radja", "Ikhlas", "LKjhakjsfh ajkhkjgabsmngbm............")
    commit()
    for i in get_data():
        print(i)
    close_all()
