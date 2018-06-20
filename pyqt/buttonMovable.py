#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtGui

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

from bdd.database_search_engine import SQL_query
import InfoFromText


class Button(QPushButton):

    def __init__(self, title, parent, cluster, app=None):
        super(Button, self).__init__(title, parent)
        self.cluster = cluster
        self.title = title
        self.app = app

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)

    def mouseDoubleClickEvent(self, e):
        QPushButton.mouseDoubleClickEvent(self, e)
        if e.button() == Qt.LeftButton:
            self.info = InfoNode(self.title, self.cluster, app=self.app)
            self.info.show()



class Example(QWidget):
    def __init__(self):
        super(Example,self).__init__()

        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)
        self.button = Button('Button', self)
        self.button.move(100, 65)
        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 150)


    def dragEnterEvent(self, e):

        e.accept()


    def dropEvent(self, e):

        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()



class InfoNode(QDialog):
    def __init__(self, name = None, articles = None, app=None):
        super(InfoNode, self).__init__()
        self.path = os.path.abspath(__file__).replace("pyqt\\buttonMovable.pyc", "")
        self.path = self.path.replace("pyqt\\buttonMovable.py", "")
        self.app = app  # QApplication для смены язык
        self.setWindowTitle(name)
        # динамически загружает визуальное представление формы
        uic.loadUi(self.path + "mallFiles/uiFiles/infoNode.ui", self)
        self.label.setText(name.replace(" ", "\n"))
        self.label.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        lan = ["RU" if "RUtexts" in i[1] else "EN" for i in articles]
        articles1 = set(
            [os.path.basename(i).replace(".txt", "")
                 for i in
             articles])

        self.textBrowser.setText("\n".join(articles1))
        dbInfo = self.getDBInfo(name, list(set([j[1] for j in articles])),lan)
        self.textBrowser_2.setText(dbInfo[0])
        self.textBrowser_3.setText(dbInfo[1])
        self.textBrowser_4.setText(dbInfo[2])
        self.textBrowser_5.setText(dbInfo[3])
        self.textBrowser_6.setText(dbInfo[4])


    def getDBInfo(self, name, texts, lan):
        self.sql = SQL_query()
        self.con = self.sql.connect()
        query = self.sql.select(texts)
        self.sql.cur.execute(query)  # выполняем запрос
        texts = [i[0] for i in self.sql.cur.fetchall()]  # список текстов
        query1 = self.sql.persons(alias=[name])
        self.sql.cur.execute(query1)
        persons = [i[1] for i in self.sql.cur.fetchall()]
        listOfSent = list(set(InfoFromText.getInfo(persons, ". ".join(texts),lan)))
        adjs = InfoFromText.getAdj(persons, listOfSent, lan[0])
        return ("<br><br>".join(InfoFromText.hightlighter(listOfSent,persons,adjs[0],adjs[1],adjs[2], adjs[3])),"\n\n".join(adjs[0]),"\n\n".join(adjs[1]), "\n\n".join(adjs[2]),"\n\n".join(adjs[3]))