# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget
import mainform  # подключает модуль описания формы


def main():
    app = QApplication(sys.argv)  # создаёт основной объект программы
    form = mainform.MainForm(app)  # создаёт объект формы
    form.show()  # даёт команду на отображение объекта формы и содержимого
    app.exec_()  # запускает приложение


if __name__ == "__main__":
    sys.exit(main())

