import sqlite3
import sys
import traceback

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QDialog


class EditDB(QDialog):
    def __init__(self):
        super(EditDB, self).__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)

    def accept(self) -> None:
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute('INSERT INTO coffee(Name, Roasting, Type, Taste, Price, Size) VALUES (?,?,?,?,?,?)',
                    [self.NameLineEdit.text(), self.RoastingLineEdit.text(), self.TypeLineEdit.text(),
                     self.TasteLineEdit.text(), self.PriceLineEdit.text(), self.SizeLineEdit.text()])
        con.commit()
        con.close()
        self.done(0)

    def reject(self) -> None:
        self.done(0)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)
        self.table()
        self.addInfoButton.clicked.connect(self.run)

    def run(self) -> None:
        sys.excepthook = except_hook
        EDB = EditDB()
        EDB.show()
        EDB.exec()
        self.table()

    def table(self) -> None:
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
        con.close()



def except_hook(cls, exception, trace):
    tb = "".join(traceback.format_exception(cls, exception, trace))
    print(tb)


# Точка входа (Entry point)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    win = Window()
    win.show()
    sys.exit(app.exec())
