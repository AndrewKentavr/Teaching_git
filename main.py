import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [600, 630]

from map import *


class Example(QWidget):
    def __init__(self):
        super().__init__()
        getImage()
        self.initUI()

    def initUI(self):
        self.setGeometry(550, 250, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.search_map = QLineEdit(self)
        self.search_map.move(0, 10)
        self.search_map.resize(350, 25)

        self.adress_map = QLineEdit(self)
        self.adress_map.move(0, 45)
        self.adress_map.resize(350, 25)

        self.search_btn = QPushButton("Искать", self)
        self.search_btn.move(370, 10)
        self.search_btn.resize(120, 25)
        self.search_btn.clicked.connect(self.search)

        self.post_index = QPushButton("Почтовый индекс", self)
        self.post_index.move(370, 45)
        self.post_index.resize(120, 25)

        self.cleat_btn = QPushButton("Очистить", self)
        self.cleat_btn.move(520, 10)
        self.cleat_btn.resize(70, 25)
        self.cleat_btn.clicked.connect(self.clear)


        self.pixmap = QPixmap(Globals.map_file)
        self.image = QLabel(self)
        self.image.move(0, 180)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def search(self):
        text = ''
        text += self.search_map.text().lower()
        Globals.longitude, Globals.latitude = geocoder_response(text)[0]
        Globals.params['pt'] = f'{Globals.longitude},{Globals.latitude},pm2orl'
        adress = geocoder_response(text)[1]

        self.adress_map.setText(adress)
        getImage()
        self.pixmap = QPixmap(Globals.map_file)
        self.image.setPixmap(self.pixmap)

    def clear(self):
        self.adress_map.setText("")
        self.search_map.setText("")
        Globals.params = {'l': 'map'}

        getImage()
        self.pixmap = QPixmap(Globals.map_file)
        self.image.setPixmap(self.pixmap)


    def closeEvent(self, event):
        os.remove(Globals.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
