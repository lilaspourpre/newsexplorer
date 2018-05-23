#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import codecs
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDialog
from PyQt5 import QtCore, uic

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
        #self.pushButton4.clicked.connect(self.openGraph)  # построение графа при нажатии кнопки "Build Graph"
        self.pushButton_ct.clicked.connect(self.del_table)  # очистка таблицы при нажатии кнопки "Clear table"
        self.pushButton_2.clicked.connect(self.fixText)  # фиксация текста, обработка запроса при нажатии кнопки "Enter"
        self.lineEdit.returnPressed.connect(
            self.fixText)  # фиксация текста, обработка запроса при нажатии клавиши "Enter" на клавиатуре
        self.pushButton_cl.clicked.connect(
            self.listWidget.clear)  # очистка истории запросов при нажатии кнопки "Clear history"
        #self.listWidget.itemDoubleClicked.connect(self.choose_text)  # реализация запроса, хранящегося в истории запроса
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
        self.changeLang(self.path + 'mallFiles/translationFiles/ru_translation.qm')  # установка языка

    def changeLangE(self):
        self.actionRussian.setChecked(False)
        self.actionEnglish.setChecked(True)  # выбран английский язык, остальные не выбраны
        self.actionFrench.setChecked(False)
        self.changeLang('en')  # установка языка

    def changeLangF(self):
        self.actionRussian.setChecked(False)
        self.actionEnglish.setChecked(False)
        self.actionFrench.setChecked(True)  # выбран французский язык, остальные не выбраны
        self.changeLang(self.path + 'mallFiles/translationFiles/fr_translation.qm')  # установка языка

    def changeLang(self, lang):
        self.lang = lang
        try:
            self.app.removeTranslator(self.translator)  # модель перевода удаляется
            self.app.removeTranslator(self.common_translator)
        except:
            pass
        if lang != 'en':  # если выбран не английский
            self.translator = QtCore.QTranslator()  # вызывается переводчик
            self.translator.load(lang)  # загружается перевод
            self.app.installTranslator(self.translator)  # переводчик устанавливается в приложение

            self.common_translator = QtCore.QTranslator()  # вызывается переводчик
            if 'fr_' in lang:
                self.lang = 'fr'
                load = self.path + 'mallFiles/translationFiles/qt_fr.qm'  # загружается перевод
            elif 'ru_' in lang:
                self.lang = 'ru'
                load = self.path + 'mallFiles/translationFiles/qt_ru.qm'
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
        " удаляем таблицу из окна просмотра таблиц "
        table_model = MyTableModel([[]], [], self)  # формируем пустую модель
        self.tableView.setModel(table_model)  # устанавливаем пустую модель

    def fixText(self):
        "фиксация текса со строки запроса"
        text = self.lineEdit.text()
        self.request(text)  # посылаем запрос в БД
        self.listWidget.addItem(text)  # добавляем текст запроса в историю запросов
        self.lineEdit.clear()  # очищаем строку запроса

    def openDialog(self):
        self.openNewWindow = DialogForm(self, text=self.text,
                                        app=self.app)  # открытие диалоговой формы, где text = [name, lang]
        self.openNewWindow.show() #показать окно

    #def openGraph(self):
    #    self.openGraphPrinter.show()  # функция ужке вызвана в _init_, здесь происходит только открытие окна

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
        # динамически загружает визуальное представление формы
        # fname = self.getOpenFileName(self)
        # if len(fname) > 5:
        #     result = self.openAnswer("Press ok to start loading", fname)
        #     self.openResult(result, fname)


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
