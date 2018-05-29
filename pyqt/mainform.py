#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import codecs
import os
from graphform import GraphForm
from AddingToDatabase import AddingToDatabase
from articles.NerAndClusering import EN_ner, RU_ner
from articles.NerAndClusering.aggClustLink import Clustering
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDialog
from PyQt5 import QtCore, uic
from bdd import request_parser

class MainForm(QMainWindow):
    # конструктор
    def __init__(self, app):
        super(MainForm, self).__init__()
        self.path = os.path.abspath(__file__).replace("\\pyqt\\mainform.pyc", "")
        self.path = self.path.replace("\\pyqt\\mainform.py", "")
        self.app = app  # QtApplication для смены языка
        self.lang = 'en'
        uic.loadUi(self.path + "\\mallFiles\\uiFiles\\first.ui",
                   self)  # загружает UIfile QtDesigner, интерфейс программы
        self.setWindowTitle(self.app.translate('MainWindow', 'Query Window'))  # заголовок главного окна
        self.lineEdit.setPlaceholderText(
            self.app.translate('MainWindow', 'Write your query here'))  # текст незаполненной строки ввода
        self.text = ['', '']  # форма для открытия окна загрузки статьи вида: [articleName, language]
        self.pushButton4.setDisabled(True)  # кнопка "построить граф" неактивна до соответствующего запроса"
        self.pushButton8.clicked.connect(self.openDialog)  # открытие диалогового окна при нажатии кнопки "Upload"
        self.pushButton4.clicked.connect(self.openGraph)  # построение графа при нажатии кнопки "Build Graph"
        self.pushButton_ct.clicked.connect(self.del_table)  # очистка таблицы при нажатии кнопки "Clear table"
        self.pushButton_2.clicked.connect(self.fixText)  # фиксация текста, обработка запроса при нажатии кнопки "Enter"
        self.lineEdit.returnPressed.connect(
            self.fixText)  # фиксация текста, обработка запроса при нажатии клавиши "Enter" на клавиатуре
        self.pushButton_cl.clicked.connect(
            self.listWidget.clear)  # очистка истории запросов при нажатии кнопки "Clear history"
        self.listWidget.itemDoubleClicked.connect(self.choose_text)  # реализация запроса, хранящегося в истории запроса
        self.pushButton_3.clicked.connect(self.openHelp)  # вызов справки при нажатии кнопки "Help"
        # возможность отмечать флагом выбранный язык
        self.actionEnglish.setCheckable(True)
        self.actionRussian.setCheckable(True)
        self.actionFrench.setCheckable(True)
        self.actionEnglish.setChecked(True)  # английский язык - язык интерфейса по умолчанию
        # смена языка при выборе языка в контекстном меню (R = Russian, E = English, F = French)
        self.actionRussian.triggered.connect(self.changeLangR)
        self.actionEnglish.triggered.connect(self.changeLangE)
        self.actionFrench.triggered.connect(self.changeLangF)

    def changeLangR(self):
        self.actionRussian.setChecked(True)  # выбран русский язык, остальные не выбраны
        self.actionEnglish.setChecked(False)
        self.actionFrench.setChecked(False)
        self.changeLang(self.path + '/mallFiles/translationFiles/ru_translation.qm')  # установка языка

    def changeLangE(self):
        self.actionRussian.setChecked(False)
        self.actionEnglish.setChecked(True)  # выбран английский язык, остальные не выбраны
        self.actionFrench.setChecked(False)
        self.changeLang('en')  # установка языка

    def changeLangF(self):
        self.actionRussian.setChecked(False)
        self.actionEnglish.setChecked(False)
        self.actionFrench.setChecked(True)  # выбран французский язык, остальные не выбраны
        self.changeLang(self.path + '/mallFiles/translationFiles/fr_translation.qm')  # установка языка

    def changeLang(self, langpath):
        self.lang = langpath
        try:
            self.app.removeTranslator(self.translator)  # модель перевода удаляется
            self.app.removeTranslator(self.common_translator)
        except:
            pass
        if langpath != 'en':  # если выбран не английский
            translator = QtCore.QTranslator()  # вызывается переводчик
            translator.load(langpath)  # загружается перевод
            self.app.installTranslator(translator)  # переводчик устанавливается в приложение
            self.common_translator = QtCore.QTranslator()  # вызывается переводчик
            if 'fr_' in langpath:
                self.lang = 'fr'
                load = self.path + '/mallFiles/translationFiles/qt_fr.qm'  # загружается перевод
            elif 'ru_' in langpath:
                self.lang = 'ru'
                load = self.path + '/mallFiles/translationFiles/qt_ru.qm'
            self.common_translator.load(load)  # загружается перевод
            self.app.installTranslator(self.common_translator)  # переводчик устанавливается в приложение
        # обновляются все символьные виджеты
        self.setWindowTitle(self.app.translate('MainWindow', 'Query Window'))  # заголовок главного окна
        self.lineEdit.setPlaceholderText(
            self.app.translate('MainWindow', 'Write your query here'))  # текст незаполненной строки ввода
        self.label.setText(self.app.translate('MainWindow',
                                              '<html><head/><body><p align="center"><span style=" font-size:11pt;">Previous queries</span></p></body></html>'))
        self.label_2.setText(self.app.translate('MainWindow',
                                                '<html><head/><body><p align="center"><span style=" font-size:11pt;">Table representation</span></p></body></html>'))
        self.pushButton_cl.setText(self.app.translate('MainWindow', 'Clear history'))
        self.pushButton_ct.setText(self.app.translate('MainWindow', 'Clear table'))
        self.pushButton4.setText(self.app.translate('MainWindow', 'Build graph'))
        self.pushButton_3.setText(self.app.translate('MainWindow', 'Help'))
        self.pushButton8.setText(self.app.translate('MainWindow', 'Upload article'))
        self.pushButton_2.setText(self.app.translate('MainWindow', 'Enter'))
        self.actionEnglish.setText(self.app.translate('MainWindow', 'English'))
        self.actionRussian.setText(self.app.translate('MainWindow', 'Russian'))
        self.actionFrench.setText(self.app.translate('MainWindow', 'French'))
        self.menuMenu.setTitle(self.app.translate('MainWindow', 'Menu'))
        self.menuChange_language.setTitle(self.app.translate('MainWindow', 'Change language'))

    def choose_text(self, item):
        self.request(item.text())  # выполняем запрос, отправляя текст, располагающийся в истории запросов

    def del_table(self):
        "удаляем таблицу из окна просмотра таблиц "
        table_model = MyTableModel([[]], [], self)  # формируем пустую модель
        self.tableView.setModel(table_model)  # устанавливаем пустую модель

    def fixText(self):
        "фиксация текса со строки запроса"
        text = self.lineEdit.text()
        self.request(text)  # посылаем запрос в БД
        self.listWidget.addItem(text)  # добавляем текст запроса в историю запросов
        self.lineEdit.clear()  # очищаем строку запроса

    def request(self, text):
        RP = request_parser.RequestParser()  # вызов парсера для формирования SQL-запроса
        try:
            RP.connect()  # установка соединения
            result = RP.request_parser(text)  # результат SQL-запроса в виде списков возвращается в переменную
            if result[0]:  # если ответ БД не пустой
                if len(result) == 3:  # если запрос был относительно связей для построения графа (дополнительный item = словарь для графа)
                    self.pushButton4.setDisabled(False)  # кнопка "Построить граф" становится активной
                    self.openGraphPrinter = GraphForm(self, req=text, clusttexts=result[2],
                                                      app=self.app)  # формируем конструктор окна
                    res_decoded = [(i[0], i[1]) for i in
                                   result[0]]  # decode для отображения русского текста
                else:
                    try:
                        res_decoded = [(i[0], i[1]) for i in
                                       result[0]]  # decode для отображения русского текста
                    except Exception as e:
                        print(e)
                        res_decoded = result[0]
                    finally:
                        self.pushButton4.setDisabled(True)  # кнопка неактивна, если запрос не по графам
            else:
                res_decoded = ['' for i in range(
                    len(result[1]))]  # если запрос нулевой, то мы возвращаем пустую строку и названия столбцов
                self.pushButton4.setDisabled(True)  # кнопка также неактивна, так как запрос пустой
            table_model = MyTableModel(res_decoded, result[1], self)  # формируем модель для просмотра таблицы
        except Exception as e:
            print(e)
            table_model = MyTableModel([['Verify the query']], ['Error'], self)
        finally:
            self.tableView.setModel(table_model)  # устанавливаем модель
        try:
            RP.close()  # закрываем соединение
        except psycopg2.DatabaseError as e:
            print(e)

    def openDialog(self):
        self.openNewWindow = DialogForm(self, text=self.text,
                                        app=self.app)  # открытие диалоговой формы, где text = [name, lang]
        self.openNewWindow.show() #показать окно

    def openGraph(self):
        self.openGraphPrinter.show()  # функция ужке вызвана в _init_, здесь происходит только открытие окна

    def openHelp(self):
        self.openHelpWindow = HelpForm(self, app=self.app,
                                       lan=self.lang)  # вызов конструктора диалогового окна по построению графа
        self.openHelpWindow.show()  # функция ужке вызвана в _init_, здесь происходит только открытие окна

class MyTableModel(QtCore.QAbstractTableModel):
    """
    создание модели для отображения таблицы
    """

    def __init__(self, datain, colnames, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.arraydata = datain  # строки результата
        self.colLabels = colnames  # имена столбцов

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.arraydata)  # подсчет количества строк

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.arraydata[0])  # подсчет количества столбцов

    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            return self.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arraydata[QModelIndex.row()][QModelIndex.column()])

    def headerData(self, p_int, Qt_Orientation, role=None):
        if Qt_Orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.colLabels[p_int])
        return QtCore.QVariant()


class DialogForm(QFileDialog):
    """
    конструктор диалогового окна по загрузке статьи
    """

    def __init__(self, parent=None, text=None, app=None):
        self.path = os.path.abspath(__file__).replace("pyqt\\mainform.pyc", "")
        self.path = self.path.replace("pyqt\\mainform.py", "")
        super(DialogForm, self).__init__(parent)
        self.app = app  # QtApplication для смены языка
        self.setWindowTitle(self.app.translate('Dialog', 'Upload Window'))  # Изменение названия окна
        self.setFileMode(QFileDialog.ExistingFiles)
        #динамически загружает визуальное представление формы
        fname = self.getOpenFileName(self)
        if len(fname[0]) > 5:
            result = self.openAnswer("Press ok to start loading", fname[0])
            self.openResult(result, fname[0])

    def openAnswer(self, text, fname, n_clusters=None):
        """
        выбор файла и его кластеризация
        :return: окно с результатом загрузки
        """
        self.openNewAnswer = AnswerForm(self, text, app=self.app)
        self.openNewAnswer.exec_()
        self.openNewAnswer.setVisible(True)
        self.openNewAnswer.label.setText("LOADING")
        self.openNewAnswer.update()
        self.openNewAnswer.repaint()
        self.openNewAnswer.doAction(0, 50)
        clusters = self.openNewAnswer.uploading(fname, n_clusters)
        self.openNewAnswer.doAction(51, 100)
        self.openNewAnswer.close()
        return clusters

    def openResult(self, resClusters, fname=None):
        self.uploadForm = UploadForm(self, resClusters[1], fname, app=self.app)
        self.uploadForm.exec_()
        self.uploadForm.setVisible(True)
        clusters = self.uploadForm.closing()
        if type(clusters) == int:
            cl = Clustering()
            if "RUtexts" in fname:
                ret = cl.namesClustering(resClusters[0], True, clusters)  # clustering them
            else:
                ret = cl.namesClustering(resClusters[0], False, clusters)  # clustering them

            self.openResult((resClusters[0], ret), fname)
        else:
            clusters = self.clust_parser(self.uploadForm.newText)
            add = AddingToDatabase()
            text_id = add.mainAddFunc(fname)
            add.close()
            self.eviterLesDoublons(clusters, text_id)
        self.uploadForm.setVisible(False)

    def eviterLesDoublons(self, clusters, text_id):
        UP = request_parser.UploadParser()
        self.copies = UP.verify_clusters(clusters)  # проверка кластеров, существуют ли они уже в списке кластеров
        if self.copies != []:  # если совпадения-таки обнаружены
            copy = ''
            for name in self.copies:  # добавляем имена в строку
                for var in name:
                    for val in var:
                        copy += str(val) + ', '
                    copy += '\n'
            self.openUpload(copy.replace(', \n', '\n'))
            copies = self.clust_replacement(self.openNewForm.newText)  # обработать имеющиеся кластеры
        self.answer = UP.return_result(clusters,
                                       text_id,
                                       copies)  # вернуть кластеры для записи, а также копии, которые необходимо использовать

    def openUpload(self, info):
        self.openNewForm = ClusterForm(self, info, app=self.app)
        self.openNewForm.exec_()

    def clust_parser(self, clust_list):
        """
        разделить список кластеров на отдельные кластеры
        clust_list: список кластеров
        """
        clusters = {}
        for i in clust_list:
            if i != u'':
                splitter = i.split(' :: ')
                clusters[splitter[0]] = splitter[1].split(', ')
        return clusters

    def clust_replacement(self, clust_list):
        """
        создает словарь кластеров для замены
        """
        dic_copies = {}
        if clust_list[len(clust_list) - 1] == u'':
            del clust_list[len(clust_list) - 1]  # удаляем u''
        for clust in clust_list:
            a = clust.split(', ')  # делим по ', '
            dic_copies[a[1]] = int(a[0])  # добавляем в словарь кластер : id
        return dic_copies


class ClusterForm(QDialog):
    def __init__(self, parent=None, text=None, app=None):
        super(ClusterForm, self).__init__(parent)
        self.state = False
        self.app = app  # QApplication для смены языка
        # динамически загружает визуальное представление формы
        self.path = os.path.abspath(__file__).replace("pyqt\\mainform.pyc", "")
        self.path = self.path.replace("pyqt\\mainform.py", "")
        uic.loadUi(self.path + "mallFiles/uiFiles/load2.ui", self)
        self.setModal(True)
        self.setWindowTitle(self.app.translate('Loading', 'Loading Window'))  # Изменение названия окна
        self.textEdit.setText(text)  # текст о результате загрузки
        self.pushButton.clicked.connect(self.closing)  # закрытие окна при нажатии ОК

    def closing(self):
        """
        при закрытии сохраняем текст и делим построчно
        """
        self.newText = self.textEdit.toPlainText()
        self.newText = self.newText.split('\n')
        self.close()


class AnswerForm(QDialog):
    """
    окно отчета о загрузке статьи
    """

    def __init__(self, parent=None, text=None, app=None):
        super(AnswerForm, self).__init__(parent)
        self.path = os.path.abspath(__file__).replace("pyqt\\mainform.pyc", "")
        self.path = self.path.replace("pyqt\\mainform.py", "")
        self.app = app  # QApplication для смены языка
        self.setUpdatesEnabled(True)
        # динамически загружает визуальное представление формы
        uic.loadUi(self.path + "mallFiles/uiFiles/answer.ui", self)
        self.setModal(True)
        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.setWindowTitle(self.app.translate('Answer', 'Loading'))  # Изменение названия окна
        self.label.setText(text)  # текст о результате загрузки
        self.pushButton.clicked.connect(self.close)  # закрытие окна при нажатии ОК

    def doAction(self, start, end):
        self.completed = start
        while self.completed < end:
            self.completed += 0.1
            self.progressBar.setValue(self.completed)

    def uploading(self, fname, n_clusters=None):

        if "RUtexts" in fname:
            ruNERc = RU_ner.ruNER()
            names = ruNERc.character_recognition(fname)
            return (names, self.specClustering(n_clusters, names, True))
        else:
            enNERc = EN_ner.enNER()
            names = enNERc.character_recognition(fname)
            return (names, self.specClustering(n_clusters, names, False))

    def specClustering(self, n_clusters, names, lang):
        cl = Clustering()
        if lang:
            return cl.namesClustering(names, True, n_clusters)  # clustering them
        else:
            return cl.namesClustering(names, False, n_clusters)  # clustering them


class UploadForm(QDialog):
    """
    окно отчета о загрузке этапа
    """

    def __init__(self, parent=None, clusters=None, fname=None, app=None):
        super(UploadForm, self).__init__(parent)
        self.clusters = clusters
        self.path = os.path.abspath(__file__).replace("pyqt\\mainform.pyc", "")
        self.path = self.path.replace("pyqt\\mainform.py", "")
        if type(clusters) == dict:
            self.text = self.update(clusters)
        else:
            self.text = clusters
        self.state = False
        self.app = app  # QApplication для смены языка
        # динамически загружает визуальное представление формы
        uic.loadUi(self.path + "mallFiles/uiFiles/load.ui", self)
        self.setModal(True)
        self.setWindowTitle(self.app.translate('Loading', 'Loading Window'))  # Изменение названия окна
        self.textEdit.setText(self.text)
        self.spinBox.setValue(len(clusters))
        self.pushButton.clicked.connect(self.close)

    def closing(self):
        """
        при закрытии сохраняем текст и делим построчно
        """
        if self.checkBox.isChecked() == True:
            self.newText = self.textEdit.toPlainText()
            self.newText = self.newText.split('\n')
            return self.clusters
        else:
            n_clusters = self.spinBox.value()
            return n_clusters

    def update(self, text):
        """
        если на вход передали словарь, то ддля его отображения на экране в форме: слово :: варианты слова в тексте,
        необходимо произвести обработку вывода
        """
        new_text = ''
        for i in text:
            new_text += i + ' :: ' + ', '.join(text[i]) + '\n\n'
        return new_text


class HelpForm(QDialog):
    """
    конструктор окна помощи
    """
    def __init__(self, parent=None, app=None, lan='en'):
        super(HelpForm, self).__init__(parent)
        self.path = os.path.abspath(__file__).replace("pyqt\\mainform.pyc", "")
        self.path = self.path.replace("pyqt\\mainform.py", "")
        self.app = app  # QApplication для смены язык
        # динамически загружает визуальное представление формы
        uic.loadUi(self.path + "mallFiles/uiFiles/help.ui", self)
        self.setWindowTitle(self.app.translate('Help', 'Help Window'))  # установка заголовка окна
        text_help = codecs.open(self.path + 'mallFiles/manualFiles/manual_' + lan + '.html', 'r', 'utf-8').read()
        self.textBrowser.setText(text_help)  # здесь располагается текст справки
