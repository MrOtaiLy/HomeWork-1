import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic

class CoffeeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_data()

    def load_data(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        if result:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            for i, row in enumerate(result):
                for j, val in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        con.close()

def main():
    app = QApplication(sys.argv)
    window = CoffeeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
