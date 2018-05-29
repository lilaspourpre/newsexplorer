# -*- coding: utf-8 -*-
import codecs
import sqlite3

from bdd.database_search_engine import SQL_query


class AddingToDatabase:
    def __init__(self):
        self.sql = SQL_query()
        self.con = self.sql.connect()

    def mainAddFunc(self, fname):
        print("mainAddFunc")
        self.idText = self.completeText(fname)
        print("textDone")
        return self.idText

    def completeText(self, fname):
        print(fname)
        text = codecs.open(fname, 'r', 'utf-8').read()
        text = text.replace(u"—", u"-")
        text = text.replace('\"', "")
        text = text.replace("'", "")
        id = self.sql.insert("texts",column_names=["textname","source"],values=[fname,text])
        print(id)
        return id

    def completeClusters(self, clusters):
        for i in clusters.keys():
            clustId = self.sql.insert("clusters", ["alias"], values=[i])
            print(clustId)
            self.completePersons(clusters[i], clustId)

    def completePersons(self, clusters, clustId):
        for val in clusters:
            persId = self.sql.insert("persons",column_names=["persname", "clustid"], values=[val, clustId])
            print(persId)
            self.completePTrel(persId)

    def completePTrel(self, persId):
        self.sql.insert("ptrelations",column_names=["personid", "textid"], values=[persId,self.idText])

    def close(self):
        try:
            self.sql.close()
        except sqlite3.DatabaseError as e:
            print(e)


