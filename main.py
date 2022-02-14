import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QDialog


class EditDB(QDialog):
    def __init__(self):
        super(EditDB, self).__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.buttonBox.clicked.connect(self.run)

    def run(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute('INSERT INTO coffee(Name, Roasting, Type, Taste, Price, Size) VALUES (?,?,?,?,?,?)',
                    [self.NameLineEdit, self.RoastingLineEdit, self.TypeLineEdit,
                     self.TasteLineEdit, self.PriceLineEdit, self.SizeLineEdit])
        con.commit()
        self.NameLineEdit.setText('')
        self.RoastingLineEdit.setText('')
        self.TypeLineEdit.setText('')
        self.TasteLineEdit.setText('')
        self.PriceLineEdit.setText('')
        self.SizeLineEdit.setText('')
        QMessageBox.information(self, "Готово!", "Информация сохранена.", QMessageBox.Ok)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM coffee""")
        db = cur.fetchall()
        self.tableWidget.setColumnCount(len(db[0]) - 1)
        self.tableWidget.setRowCount(len(db))
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Roasting", "Type", "Taste", "Price", "Size"])
        for i, elemi in enumerate(db):
            for j, elemj in enumerate(elemi[1:]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(elemj))
        self.addInfoButton.clicked.connect(self.run)

    def run(self):
        app2 = QApplication(sys.argv)
        sys.excepthook = except_hook
        EDB = EditDB()
        EDB.show()
        app2.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# Точка входа (Entry point)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    win = Window()
    win.show()
    sys.exit(app.exec())
