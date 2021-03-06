# -*- coding: utf-8 -*-
import sqlite3
import time
import xml.etree.ElementTree as ET


class SQL_query():
    """
    класс, который осуществляет поиск в базе данных
    поддерживает возможность поиска информации и добаления новых данных (insert)
    """

    def __init__(self):
        self.con = None
        self.cur = None
        self.DB_RECONNECT_DELAY_SEC = 1

    def open_config(self, config):  # находит в файле xml код и строит дерево, возвращает строку для коннекта
        tree = ET.parse(config)
        root = tree.getroot()
        string = ""
        for child in root:  # соединяем данные в строку user=postgres и тд
            string += child.tag + "='" + child.text + "' "
        return string

    def connect(self):  # подключение к БД
        try:
            self.con = sqlite3.connect("../bdd/sqlFile/newsfeeds.db")
            self.cur = self.con.cursor()
        except sqlite3.DatabaseError as e:
            print(e)
            if self.con:
                self.con.rollback()

    def close(self):  # отключение от БД
        if self.con:
            self.con.close()

    def ensure_connection(self):
        while not self.con:
            self.connect()
            if not self.con:
                # wait for a second
                time.sleep(self.DB_RECONNECT_DELAY_SEC)

    def __select_condition(self, columnname, data):
        """
        вспомогательная функция для Texts, Persons, Clusters (поиска по БД)
        :param columnname: название столбца указывается автоматически, пользователю его набирать не нужно
        :param data: указанное значение
        :return: соединяет условие для запроса в вид persid
        """
        condition = []
        for i in data:
            condition.append(columnname + """=""" + self.checktype(i))
        return """(""" + """ OR """.join(condition) + """) AND """

    def checktype(self, inputdata):
        if type(inputdata) == int:
            return str(inputdata)
        elif type(inputdata) == str:
            if not inputdata.isdigit() and not inputdata.isdecimal():
                return '"' + inputdata + '"'
            else:
                return inputdata
        else:
            return str(inputdata)

    def texts(self, persons=None, alias=None, textname=None):
        """
        :param persons: заданные параметры persons означают, что тексты будут выдаваться относительно персонажей в них
        :param clustid: заданные параметры clustid означают, что тексты будут выдаваться относительно персонажей в них (более общее чем persons)
        :param alias: заданные параметры alias означают, что тексты будут выдаваться относительно персонажей в них
        (то же, что и clustid, только задается общее имя для кластера, а не его номер)
        :return: возвращает номер и название текста (textid, textname)
        """
        self.ensure_connection()
        query = """SELECT texts.textid, texts.textname FROM texts """
        if any([alias != None, persons != None]):
            query += """ JOIN ptrelations JOIN persons JOIN clusters ON ptrelations.personid=persons.personid AND ptrelations.textid=texts.textid AND clusters.clustid=persons.clustid"""
        query += """ WHERE """
        if alias != None:
            query += self.__select_condition("""alias""", alias)
        if persons != None:
            query += self.__select_condition("""persname""", persons)
        if textname != None:
            query += self.__select_condition("""textname""", textname)
        query += """1=1;"""
        return query

    def ptrelations(self, textid=None, personid=None):
        """
        :param textid: заданные параметры textid означают, что отношения будут выдаваться в соответствии с номером текста
        :param personid: заданные параметры personid означают, что отношения будут выдаваться в соответствии с номером персонажа
        :return: возвращает номер текста и номера имени персонажа
        """
        self.ensure_connection()
        query = """SELECT * FROM ptrelations WHERE """
        if textid != None:
            query += self.__select_condition("""textid""", textid)
        if personid != None:
            query += self.__select_condition("""personid""", personid)
        query += """1=1;"""
        return query

    def persons(self, textname=None, alias=None, personid=None):
        """
        :param clustid: заданные параметры clustid означают, что персонажи будут выдаваться в соответствии с номером кластера
        :param textid: заданные параметры textid означают, что персонажи будут выдаваться в соответствии с номером текста
        :param alias: заданные параметры alias означают, что персонажи будут выдаваться в соответствии с кластером
        (то же, что и clustid, только задается общее имя для кластера, а не его номер)
        :return: возвращает номер и имя персонажа (personid, persname)
        """
        self.ensure_connection()
        query = """SELECT persons.personid, persname"""
        if personid != None:
            query += """, clustid"""
        query += """ FROM persons JOIN clusters JOIN ptrelations JOIN texts ON ptrelations.personid=persons.personid AND ptrelations.textid=texts.textid AND clusters.clustid=persons.clustid"""
        query += """ WHERE """
        if personid != None:
            query += self.__select_condition("""personid""", personid)
        if alias != None:
            query += self.__select_condition("""alias""", alias)
        if textname != None:
            query += self.__select_condition("""textname""", textname)
        query += """1=1;"""
        return query

    def clusters(self, textname=None, persons=None, alias=None):
        """
        :param text: заданные параметры textid означают, что кластеры будут выдаваться в соответствии с номером текста
        :param persons: заданные параметры persons означают, что кластеры будут выдаваться относительно персонажей в них
        :return: возвращает номер и имя кластера персонажа
        """
        self.ensure_connection()
        if textname != None:
            query = """SELECT clusters.clustid, alias, texts.textid FROM clusters JOIN persons JOIN ptrelations JOIN texts ON ptrelations.personid=persons.personid AND ptrelations.textid=texts.textid AND clusters.clustid=persons.clustid"""
        else:
            query = """SELECT clusters.clustid, alias FROM clusters JOIN persons JOIN ptrelations JOIN texts ON ptrelations.personid=persons.personid AND ptrelations.textid=texts.textid AND clusters.clustid=persons.clustid"""
        query += """ WHERE """
        if textname != None:
            query += self.__select_condition("""textname""", textname)
        if persons != None:
            query += self.__select_condition("""persname""", persons)
        query += """1=1;"""
        if alias != None:
            query = """SELECT * FROM clusters WHERE """ + self.__select_condition("""alias""", alias) + """1=1;"""
        return query

    def insert(self, table_name, column_names=None, values=[]):
        """
        :param table_name: мы ведь должны указывать название таблицы, иначе куда делать insert
        :param column_names: и column_names тоже, по желанию
        :param values: и то, что добавить хотим
        :return: просто commit it
        """
        self.ensure_connection()
        self.cur.execute("SELECT * FROM " + table_name)
        c_name = [desc[0] for desc in self.cur.description][0]
        columns = """"""
        if column_names != None:  # если указываются, добавляем в раздел со столбцами
            assert len(column_names) == len(values)
            columns += """(""" + """, """.join(column_names) + """)"""
        condition = []
        for i in values:
            condition.append(self.checktype(i))
        print("""INSERT INTO """ + table_name + """ """ + columns + """ """ + """VALUES (""" + """, """.join(
            condition) + """)""")
        self.cur.execute("""INSERT INTO """ + table_name + """ """ + columns + """ """ + """VALUES (""" + """, """.join(
            condition) + """)""")
        id_of_new_row = self.cur.lastrowid
        self.con.commit()
        return id_of_new_row

    def delete(self, table, textid=None, clustid=None, personid=None):
        """
        :param table: имя таблицы, откуда происходит удаление
        :param textid: условия для поиска строк, которые необходимо удалить
        :param clustid: условия для поиска строк, которые необходимо удалить
        :param personid: условия для поиска строк, которые необходимо удалить
        :return: запрос для удаления
        """
        self.ensure_connection()
        query = """DELETE FROM """ + table + """ WHERE """
        if textid != None:
            query += self.__select_condition("""textid""", textid)
        if personid != None:
            query += self.__select_condition("""personid""", personid)
        if clustid != None:
            query += self.__select_condition("""clustid""", clustid)
        query += """1=1;"""
        return query

    def select(self, textname=None):
        """
        :param persons: заданные параметры persons означают, что тексты будут выдаваться относительно персонажей в них
        :param clustid: заданные параметры clustid означают, что тексты будут выдаваться относительно персонажей в них (более общее чем persons)
        :param alias: заданные параметры alias означают, что тексты будут выдаваться относительно персонажей в них
        (то же, что и clustid, только задается общее имя для кластера, а не его номер)
        :return: возвращает номер и название текста (textid, textname)
        """
        self.ensure_connection()
        query = """SELECT source FROM texts """
        query += """WHERE """
        if textname != None:
            query += self.__select_condition("""textname""", textname)
        query += """1=1;"""
        return query
