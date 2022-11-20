import sqlite3
import sys
from random import randint

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.con = sqlite3.connect('coffee.sqlite.db')
        self.cur = self.con.cursor()
        self.res = self.cur.execute("""SELECT * FROM coffee""").fetchall()
        title = ['ID', 'название сорта', 'степень обжарки',
                 'молотый/в зернах', 'описание вкуса', 'цена', "объем упаковки"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
