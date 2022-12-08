import sqlite3
import sys
from random import randint

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

names = {0: 'id',
         1: 'variety_name',
         2: 'degree_of_roast',
         3: 'ground_or_in_grains',
         4: 'taste_description',
         5: 'price',
         6: 'packing_volume'}


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class exam(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.sqlite.db')
        self.pushButton.clicked.connect(self.new)
        self.cur = self.con.cursor()
        self.select()
        self.all = []

    def new(self):
        self.cur.execute(
            f"""INSERT INTO coffee(variety_name, degree_of_roast, ground_or_in_grains, taste_description,
             price, packing_volume) VALUES('', '', '', '', '', '')""")

        self.con.commit()
        self.select()
        ex.select()

    def update_check(self, current):
        d = f'{names[current.column()]} = "{current.text()}"'
        # self.all.append((f'{names[current.column()]} = "{current.text()}"', current.row() + 1))
        self.cur.execute(
            f"UPDATE coffee SET {d} WHERE id == {current.row() + 1}")
        self.con.commit()
        ex.select()

    def select(self):
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

        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.con = sqlite3.connect('coffee.sqlite.db')
        self.cur = self.con.cursor()
        self.w1 = exam()

        self.select()
        self.pushButton.clicked.connect(self.edit)

    def edit(self):
        self.w1.show()
        self.w1.tableWidget.itemChanged.connect(self.w1.update_check)

    def select(self):
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

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
