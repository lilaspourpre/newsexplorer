from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import uic
import os
import random
import math
import codecs
from buttonMovable import Button
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, )
import InfoFromText
from bdd.database_search_engine import SQL_query


class GraphForm(QDialog):
    """
    конструктор окна с графом
    """

    def __init__(self, parent=None, req=None, clusttexts=None, app=None):
        super(GraphForm, self).__init__(parent)
        self.path = os.path.abspath(__file__).replace("pyqt\\graphform.py", "")
        self.path = self.path.replace("pyqt\\mainform.py", "")
        self.app = app  # QApplication для смены языка
        self.req = req  # текст запроса = название файлов
        self.text = ''
        self.clusttexts = clusttexts  # словарь с именами и статьями для каждго имени
        # динамически загружает визуальное представление формы
        uic.loadUi(self.path + "mallFiles/uiFiles/graph.ui", self)
        self.setWindowTitle(self.app.translate('Graph', 'Graph Window'))  # Изменение названия окна
        self.sc = MyStaticMplCanvas(self.widget, width=5, height=4, dpi=100, req=req,
                                    clusttexts=self.clusttexts)  # отображение графа в QWidget
        self.verticalLayout.addWidget(self.sc)  # добавление виджета sc - основа графа
        self.widget.setFocus()  # элемент компоновки
        self.pushButton.clicked.connect(self.setBrowserText)  # отображение свойств графа при нажатии клавиш
        self.pushButton_5.clicked.connect(self.saveGraph)  # сохранить граф в папку Graphs
        self.pushButton_7.clicked.connect(
            self.saveAll)  # сохранить граф в папку Graphs, а информацию по графу в папку Info
        self.pushButton_2.clicked.connect(self.openGB)

    def openGB(self):
        self.g = GraphButtonWindow(self.clusttexts, self.app)
        self.g.show()

    def setBrowserText(self):
        """
        :return: свойства графа
        """
        text = self.sc.graph_parameters()  # возвращает свойства графа
        self.textBrowser.setText(text)

    def saveGraph(self):
        """
        :return: изобрание в папке Graphs
        """
        self.sc.build_graph()

    def saveAll(self):
        """
        сохранить граф в виде изображение и текстовое описание свойств графа
        :return: изобрание графа в папке Graphs, текстовый файл в папке Graphs/Info
        """
        self.sc.saveText()  # вызов функции по сохранению информации о графе
        if os.path.exists('out/Graphs/' + self.req + ".png"):  # если файл еще не создан, то сохранить изображение
            pass
        else:
            self.saveGraph()

class MyMplCanvas(FigureCanvas):
    """Основа для отображения графа"""

    def __init__(self, parent=None, width=5, height=4, dpi=100, req=None, clusttexts=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.req = req  # текст запроса (для имени изображения
        self.clusttexts = clusttexts  # кластеры для построения графа (подлежат обработке)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        self.G = nx.Graph()  # вызов графа
        dic = self.buildEdges(self.clusttexts)  # преобразование в форму [text, [name1,name2,name3]]
        self.lwidth = self.widthGr(dic)
        bc = nx.betweenness_centrality(self.G)
        # self.bc = [(bc[i]+0.005) * 50000 for i in G.nodes()]  #betweenness centrality для каждой вершины
        self.bc = [math.log((bc[i] + 0.005) * 300) * 400 for i in self.G.nodes()]
        # self.bc = [500 * math.log(10000 * bc[i]) if bc[i] > 0.000001 else 10 for i in G.nodes()]
        cc = nx.closeness_centrality(self.G)
        self.cc = [cc[i] for i in self.G.nodes()]  # closeness_centrality для каждой вершины
        self.degree = nx.degree(self.G)
        try:
            self.diameter = nx.diameter(self.G)
        except:
            pass
        self.clustering = nx.average_clustering(self.G)
        self.density = float(len(nx.edges(self.G))) / ((len(nx.nodes(self.G)) - 1) * len(nx.nodes(self.G)) / 2)
        nx.draw(self.G, node_size=self.bc, node_color=self.cc, with_labels=True, width=self.lwidth,
                edge_color='DarkCyan', alpha=0.4, font_family='verdana', font_size=10, ax=self.axes)

    def buildEdges(self, clusttexts):
        """
        :param clusttexts: словарь, героев и список их текстов
        :return: список текстов и героев в каждом из них
        """
        texts = list(set([el for lst in clusttexts.values() for el in lst]))  # создаем список текстов
        allTexts = []  # пустой список для хранения в формате [text, [pers1,pers2,pers3]]
        for text in texts:
            l = []  # список персонажей
            for cluster in clusttexts:  # для каждого персонажа
                if text in clusttexts.get(cluster):  # если он упоминается в тексте
                    l.append(cluster)  # персонаж вносится в список
            allTexts.append([text, l])  # сохранение в формате [text, [pers1,pers2,pers3]]
        return allTexts

    def widthGr(self, dic):
        list_of_edges = []
        list_of_width = []
        for i in dic:  # для каждого текста
            for j in i[1]:  # для каждого героя в тексте
                for k in i[1]:  # с каждым героем в тексте
                    list_of_edges.append((j, k))
        new_list_of_edges = set(list_of_edges)
        for i in new_list_of_edges:
            self.G.add_edge(i[0], i[1])  # строится ребро
        for i in self.G.edges():
            list_of_width.append(list_of_edges.count(i) + list_of_edges.count((i[1], i[0])))
        return list_of_width

    def graph_parameters(self):
        """
        :return: текст с парамтерами графа
        """
        text = 'query: ' + self.req + '\n'
        text += "betweenness centrality = " + str(self.bc) + '\n'
        text += "closeness centrality = " + str(self.cc) + '\n'
        try:
            text += "diameter = " + str(self.diameter) + '\n'
        except:
            pass
        text += "average clustering = " + str(self.clustering) + '\n'
        text += "degree = " + str(self.degree) + '\n'
        text += "density = " + str(self.density)
        return text

    def build_graph(self):
        nx.draw(self.G, node_size=self.bc, node_color=self.cc, width=self.lwidth, with_labels=True, font_size=10,
                edge_color='DarkCyan', alpha=0.4, font_family='verdana')  # построение графа
        plt.savefig('out/Graphs/' + self.req + '.png')  # сохранение графа в папку Graphs

    def saveText(self):
        """
        :return: txt файл с параметрами графа
        """
        text = self.graph_parameters()
        with codecs.open('Graphs/Info/' + self.req + '.txt', 'w', encoding='utf-8') as wr:
            wr.write(text)


class GraphButtonWindow(QtWidgets.QMainWindow):
    """
        конструктор окна с графом
    """

    def __init__(self, clusttexts=None, app=None):
        super(GraphButtonWindow, self).__init__()
        self.path = os.path.abspath(__file__).replace("pyqt\\graphform.py", "")
        self.path = self.path.replace("pyqt\\graphform.py", "")
        self.app = app  # QApplication для смены язык
        self.setWindowTitle(self.app.translate("Graph representation", 'Graph Window'))
        self.resize(640, 480)
        # динамически загружает визуальное представление формы
        uic.loadUi(self.path + "mallFiles/uiFiles/graph2.ui", self)
        self.randoms = {}
        self.assoBtn = {}
        self.setAcceptDrops(True)
        self.selectButton.clicked.connect(self.infoRelations)
        for o in clusttexts:
            btn = Button(o, self, clusttexts[o], app=self.app)
            btn.setToolTip('Click to open info!')
            btn.clicked.connect(self.infoNodes(o, clusttexts[o], btn))
            btn.resize(len(o) * 3 + 50, 30)
            cl = (random.randint(50, 600), random.randint(50, 430))
            btn.move(cl[0], cl[1])
            self.randoms[btn] = cl
            self.assoBtn[o] = btn
        self.prevPos = self.defineEdges(clusttexts)
        self.listOfNamesPairs = []
        self.listOfClustersPairs = []
        self.listOfButtons = []

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        q = e.source()
        q.move(position)
        self.randoms[q] = (q.x(), q.y())
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
        self.update()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(75, 51, 85, 127)
        pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        self.painPaths = []
        for i in self.prevPos:
            for j in self.prevPos:
                s = i[0]
                e = i[1]
                rstart = self.assoBtn[s]
                rend = self.assoBtn[e]
                start = QtCore.QPointF(self.randoms[rstart][0], self.randoms[rstart][1])
                endPoint = QtCore.QPointF(self.randoms[rend][0], self.randoms[rend][1])
                cubicPath = QtGui.QPainterPath(start)
                cubicPath.lineTo(endPoint)
                painter.drawPath(cubicPath)

    def defineEdges(self, clusttexts):
        dic = self.buildEdges(clusttexts)
        list_of_edges = []
        for i in dic:  # для каждого текста
            for j in i[1]:  # для каждого героя в тексте
                for k in i[1]:  # с каждым героем в тексте
                    list_of_edges.append((j, k))
        return list_of_edges

    def buildEdges(self, clusttexts):
        """
        :param clusttexts: словарь, героев и список их текстов
        :return: список текстов и героев в каждом из них
        """
        texts = list(set([el for lst in clusttexts.values() for el in lst]))  # создаем список текстов
        allTexts = []  # пустой список для хранения в формате [text, [pers1,pers2,pers3]]
        for text in texts:
            l = []  # список персонажей
            for cluster in clusttexts:  # для каждого персонажа
                if text in clusttexts.get(cluster):  # если он упоминается в тексте
                    l.append(cluster)  # персонаж вносится в список
            allTexts.append([text, l])  # сохранение в формате [text, [pers1,pers2,pers3]]
        return allTexts

    def removePairs(self, name, clust, btn):
        self.listOfNamesPairs.remove(name)
        self.listOfClustersPairs.remove(clust)
        self.listOfButtons.remove(btn)
        btn.setStyleSheet('QPushButton {'
                          'background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, '
                          'stop: 0 #C7F5E8, stop: 0.1 #8DE8CE, stop: 0.49 #6DD0B3, '
                          'stop: 0.5 #6DD0B3, stop: 1 #8DE8CE);'
                          'color: black;}')

    def infoNodes(self, name, clust, btn):
        def info():
            if name in self.listOfNamesPairs:
                self.removePairs(name, clust, btn)
            else:
                self.listOfNamesPairs.append(name)
                self.listOfClustersPairs.append(clust)
                self.listOfButtons.append(btn)
                btn.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')

        return info

    def infoRelations(self):
        self.info = InfoRelations(name=self.listOfNamesPairs, articles=self.listOfClustersPairs, app=self.app)
        for i in range(len(self.listOfNamesPairs)):
            self.removePairs(self.listOfNamesPairs[0], self.listOfClustersPairs[0], self.listOfButtons[0])
        self.info.show()


class InfoRelations(QDialog):
    def __init__(self, name=None, articles=None, app=None):
        super(InfoRelations, self).__init__()
        self.path = os.path.abspath(__file__).replace("pyqt\\graphform.pyc", "")
        self.path = self.path.replace("pyqt\\graphform.py", "")
        self.app = app  # QApplication для смены язык
        self.setWindowTitle("&".join(name))
        uic.loadUi(self.path + "mallFiles/uiFiles/infoRel.ui", self)
        self.label.setText(" &\n".join(name))
        self.label.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        resArticles = self.getArticles(articles)
        self.language = "RU" if "RU" in resArticles[0] else "EN"
        self.textBrowser.setText("\n".join(
            [text.replace("newsexplorer/articles/Documents/RUtexts/", "")
                 .replace("newsexplorer/articles/Documents/ENtexts/", "")
                 .replace(".txt", "")
             for text in resArticles]))
        self.textBrowser_2.setText("<br><br>".join(self.getDBInfo(name, resArticles, self.language)))

    def getArticles(self, articles):
        newList = []
        resList = []
        for art in articles:
            for a in art:
                newList.append(a[1])
        dictArticles = dict.fromkeys(list(set(newList)), 0)
        for person in articles:
            for article in person:
                dictArticles[article[1]] += 1
        for key in dictArticles:
            if dictArticles[key] > 1:
                resList.append(key)
        return resList

    def getDBInfo(self, names, texts, lan):
        self.sql = SQL_query()
        self.con = self.sql.connect()
        query = self.sql.select(texts)
        self.sql.cur.execute(query)  # выполняем запрос
        texts = [i[0] for i in self.sql.cur.fetchall()]  # список текстов
        personsNames = []  # listof lists of names
        listOfSent = []
        for name in names:
            query1 = self.sql.persons(alias=[name])
            self.sql.cur.execute(query1)
            personsNames.append([i[1] for i in self.sql.cur.fetchall()])
        allNames = []
        for persons in personsNames:
            allNames.extend(persons)
        for persons in personsNames:
            listOfSent.append(list(set(InfoFromText.getInfo(persons, ".\n".join(texts), lan, "true"))))
        listOfSent = self.getSent(listOfSent)
        listOfSent = InfoFromText.hightlighter(listOfSent, list(set(allNames)))
        return listOfSent

    def getSent(self, listOfSent):
        newList = []
        resList = []
        for person in listOfSent:
            for sent in person:
                newList.append(sent)
        dictArticles = dict.fromkeys(list(set(newList)), 0)
        for sent in newList:
            dictArticles[sent] += 1
        for key in dictArticles:
            if dictArticles[key] > 1:
                resList.append(key)
        return resList
