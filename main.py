import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt6 import uic

class AddEditCoffeeForm(QDialog):
    def __init__(self, coffee_id=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.coffee_id = coffee_id
        if self.coffee_id:
            self.load_coffee()
        self.saveButton.clicked.connect(self.save_data)

    def load_coffee(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        row = cur.execute('SELECT name, roast, ground, taste, price, volume FROM coffee WHERE id=?',
                          (self.coffee_id,)).fetchone()
        con.close()
        if row:
            self.nameEdit.setText(row[0])
            self.roastEdit.setText(row[1])
            self.groundCheck.setChecked(bool(row[2]))
            self.tasteEdit.setText(row[3])
            self.priceEdit.setText(str(row[4]))
            self.volumeEdit.setText(str(row[5]))

    def save_data(self):
        name = self.nameEdit.text()
        roast = self.roastEdit.text()
        ground = 1 if self.groundCheck.isChecked() else 0
        taste = self.tasteEdit.text()
        price = float(self.priceEdit.text())
        volume = int(self.volumeEdit.text())
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if self.coffee_id:
            cur.execute('''
            UPDATE coffee
            SET name=?, roast=?, ground=?, taste=?, price=?, volume=?
            WHERE id=?
            ''', (name, roast, ground, taste, price, volume, self.coffee_id))
        else:
            cur.execute('''
            INSERT INTO coffee(name, roast, ground, taste, price, volume)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, roast, ground, taste, price, volume))
        con.commit()
        con.close()
        self.accept()

class CoffeeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_data()
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute('SELECT * FROM coffee').fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Roast', 'Ground', 'Taste', 'Price', 'Volume']
        )
        for i, row in enumerate(result):
            for j, val in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        con.close()

    def add_coffee(self):
        form = AddEditCoffeeForm()
        if form.exec():
            self.load_data()

    def edit_coffee(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            return
        coffee_id = int(self.tableWidget.item(row, 0).text())
        form = AddEditCoffeeForm(coffee_id)
        if form.exec():
            self.load_data()

def main():
    app = QApplication(sys.argv)
    window = CoffeeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
