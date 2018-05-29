# -*- coding: utf-8 -*-
import database_search_engine as dse
import sqlite3

RP = dse.SQL_query()
RP.connect()
# RP.cur.execute('DROP TABLE IF EXISTS articles')



RP.cur.execute("""CREATE TABLE IF NOT EXISTS texts (textid INTEGER PRIMARY KEY AUTOINCREMENT,textname varchar NOT NULL,source varchar NOT NULL);""")

RP.cur.execute("""CREATE TABLE IF NOT EXISTS clusters (clustid INTEGER PRIMARY KEY AUTOINCREMENT, alias varchar NOT NULL);""")

RP.cur.execute("""CREATE TABLE IF NOT EXISTS persons (personid INTEGER PRIMARY KEY AUTOINCREMENT,persname varchar NOT NULL,clustid INTEGER NOT NULL, CONSTRAINT Fk_persons FOREIGN KEY (clustid) REFERENCES clusters(clustid) ON DELETE RESTRICT ON UPDATE RESTRICT);""")

RP.cur.execute("""CREATE TABLE IF NOT EXISTS ptrelations (personid INTEGER NOT NULL,textid INTEGER NOT NULL,CONSTRAINT Pk_ptrel PRIMARY KEY (personid, textid),CONSTRAINT Fk_ptrel FOREIGN KEY (personid) REFERENCES persons(personid) ON DELETE RESTRICT ON UPDATE RESTRICT,CONSTRAINT Fk_ptrel2 FOREIGN KEY (textid) REFERENCES texts(textid) ON DELETE RESTRICT ON UPDATE RESTRICT);""")

RP.con.commit()
try:
    RP.close()
except sqlite3.DatabaseError as e:
    print(e)
