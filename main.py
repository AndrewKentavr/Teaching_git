import os
import sys

from PyQt5.QtCore import Qt
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
        self.search_map.textChanged[str].connect(self.search)

        self.adress_map = QLineEdit(self)
        self.adress_map.move(0, 45)
        self.adress_map.resize(350, 25)

        # self.search_btn = QPushButton("Искать", self)
        # self.search_btn.move(370, 10)
        # self.search_btn.resize(120, 25)
        # self.search_btn.clicked.connect(self.search)

        self.post_index = QPushButton("Почтовый индекс", self)
        self.post_index.move(370, 45)
        self.post_index.resize(120, 25)
        self.post_index.clicked.connect(self.post_index_func)

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
        if text == '':
            return
        check_geocoder = geocoder_response(text)
        if check_geocoder == "IndexError":
            return
        Globals.longitude, Globals.latitude = check_geocoder[0]
        Globals.params['pt'] = f'{Globals.longitude},{Globals.latitude},pm2orl'
        Globals.adress = check_geocoder[1]
        Globals.post = check_geocoder[2]

        self.adress_map.setText(Globals.adress)
        getImage()
        self.pixmap = QPixmap(Globals.map_file)
        self.image.setPixmap(self.pixmap)

    def search_2(self, count, text):
        if text == '':
            return
        if count == 0:
            check_geocoder = photo_response(text)
        else:
            check_geocoder = organizations_response(text)
        if check_geocoder == "IndexError":
            return
        Globals.longitude, Globals.latitude = check_geocoder[0]
        Globals.params['pt'] = f'{Globals.longitude},{Globals.latitude},pm2orl'
        Globals.adress = check_geocoder[1]
        Globals.post = check_geocoder[2]

        self.adress_map.setText(Globals.adress)
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

    def post_index_func(self):
        text = ''
        text += self.search_map.text().lower()
        postal_code = Globals.post
        Globals.adress += ' || ' + postal_code
        self.adress_map.setText(Globals.adress)

    def closeEvent(self, event):
        os.remove(Globals.map_file)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            ll = self.cords(x, y)
            self.search_2(0, ll)

        elif event.button() == Qt.RightButton:
            x = event.x()
            y = event.y()
            ll = self.cords(x, y)
            self.search_2(1, ll)

    def cords(self, x, y):
        if y > 180:
            ll = str(Globals.longitude).split('.')
            la = str(Globals.latitude).split('.')
            const_x = 5.5
            const_y = 2.65

            if x < 300:
                n = (300 - int(x)) * const_x
                long = int(int(ll[1]) - n)
            else:
                n = (int(x) - 300) * const_x
                long = int(int(ll[1]) + n)

            if y < 400:
                n = (int(y) - 400) * const_y
                lat = int(int(la[1]) - n)
            else:
                n = (400 - int(y)) * const_y
                lat = int(int(la[1]) + n)

            longitude = ll[0] + '.' + str(long)
            latitude = la[0] + '.' + str(lat)

            cat = longitude + ' ' + latitude
            return cat


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
