from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from optimal_ui import Ui_optimal_widget
from hesaplama import *

max_box = 16
tekil_max_ebat = 150
tekil_min_ebat = 5
tezgah_boy = 0
tezgah_en = 0


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Setting up the widgets and layout
        self.scr = Ui_optimal_widget()
        self.scr.setupUi(self)
        self.scr.ekle_butonu.clicked.connect(self.goster)
        self.scr.clean_butonu.clicked.connect(self.temizle)
        self.scr.hesap_butonu.clicked.connect(self.optimal_hesap)
        self.rectangles = []
        self.display_rect = []
        self.rect_labels = []
        self.scr.toplam_alan.setVisible(False)
        self.scr.hesap_butonu.setVisible(False)
        self.toplam_alan = 0
        self.hesap_obj = None
        self.veri_girisi()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
        for display_rectangle in self.display_rect:
            x1 = display_rectangle[0]
            y1 = display_rectangle[1]
            x2 = display_rectangle[2]
            y2 = display_rectangle[3]
            qp.drawRect(x1, y1, x2, y2)

    def temizle(self):
        self.scr.tezgah_boy.setText("")
        self.scr.tezgah_en.setText("")
        for row in range(max_box):
            self.scr.tableWidget.setItem(row, 0, QTableWidgetItem(" "))
            self.scr.tableWidget.setItem(row, 1, QTableWidgetItem(" "))
        self.display_rect.clear()
        self.rectangles.clear()
        for i in range(len(self.rect_labels)):
            self.rect_labels[i].setText(" ")
        self.rect_labels.clear()
        self.scr.toplam_alan.setVisible(False)
        self.scr.hesap_butonu.setVisible(False)
        self.update()

    def giris_kontrol(self, tbl):
        en_boy_list = []
        max_alan = tezgah_boy * tezgah_en
        self.rectangles.clear()
        for row in range(max_box):
            for col in range(2):
                item = tbl.item(row, col)
                if item is not None:
                    if item.text() == ' ':
                        break
                    try:
                        en_boy = int(item.text())
                    except ValueError:
                        QMessageBox.about(self, "Hata", "Nümerik Değer Hatası")
                        return False
                    if en_boy >= tekil_max_ebat:
                        QMessageBox.about(self, "Hata", "En Boy " + str(tekil_max_ebat) + " mm'den küçük olmalı")
                        return False
                    elif en_boy <= tekil_min_ebat:
                        QMessageBox.about(self, "Hata", "En Boy " + str(tekil_min_ebat) + " mm'den büyük olmalı")
                        return False
                    else:
                        en_boy_list.append(en_boy)

        if len(en_boy_list) % 2 == 0:
            self.toplam_alan = 0
            q = int(len(en_boy_list) / 2)
            for i in range(q):
                en = en_boy_list[(i * 2)]
                boy = en_boy_list[(i * 2) + 1]
                self.toplam_alan += (en * boy)
                self.rectangles.append([en, boy])
            if self.toplam_alan > max_alan:
                QMessageBox.about(self, "Hata", "Girilen toplam dikdörtgen alanı sınırları aşmaktadır ")
                return False
            else:
                return True
        else:
            QMessageBox.about(self, "Hata", "Eksik Veri Girişi ... ")
            return False

    def veri_girisi(self):
        for i in range(max_box):
            self.scr.tableWidget.insertRow(i)
            self.scr.tableWidget.setRowHeight(i, 10)
        self.scr.tezgah_boy.setFocus()

    def optimal_hesap(self):
        if self.hesap_obj is not None:
            del self.hesap_obj
        if len(self.rectangles) > 0:
            self.hesap_obj = hesapla(self.pos(), self.rectangles, tezgah_boy, tezgah_en)

    def goster(self):
        global tezgah_boy
        global tezgah_en
        try:
            tezgah_boy = int(self.scr.tezgah_boy.text())
        except ValueError:
            self.scr.tezgah_boy.setText(" ")
        try:
            tezgah_en = int(self.scr.tezgah_en.text())
        except ValueError:
            self.scr.tezgah_en.setText(" ")

        if tezgah_boy <= 1 or tezgah_en <= 1 or tezgah_boy > 300 or tezgah_en > 130:
            QMessageBox.about(self, "Hata", "Tezgah Boyutları Min : 10x10mm  Max : 300x130mm olabilir ")

        else:
            tezgah_boy += 1
            tezgah_en += 1
            max_x2 = 0
            x_base = 500
            y_base = 140
            index = 0
            self.display_rect.clear()
            for i in range(len(self.rect_labels)):
                self.rect_labels[i].setText(" ")
            self.rect_labels.clear()
            if self.giris_kontrol(self.scr.tableWidget):
                x1 = x_base
                y1 = y_base
                k = 0
                for rectangle in self.rectangles:
                    y2 = rectangle[0]
                    x2 = rectangle[1]
                    if y2 > x2:
                        x2, y2 = y2, x2
                    x2 = int(x2 * 1.5)
                    y2 = int(y2 * 1.5)
                    if x2 > max_x2:
                        max_x2 = x2
                    if y1 + y2 > 610:
                        x_base = x_base + max_x2 + 20
                        x1 = x_base
                        y1 = y_base
                        max_x2 = 0
                    self.display_rect.append([x1, y1, x2, y2])
                    self.rect_labels.append(QtWidgets.QLabel(self))
                    self.rect_labels[-1].setGeometry(QtCore.QRect(x1, y1, x2, y2))
                    index += 1
                    self.rect_labels[-1].setText(str(index))
                    self.rect_labels[-1].setAlignment(QtCore.Qt.AlignCenter)
                    y1 += y2 + 5

                self.update()
                for labels in self.rect_labels:
                    labels.show()

                self.scr.toplam_alan.setText("Toplam Alan : " + str(self.toplam_alan) + " mm2")
                self.scr.toplam_alan.setVisible(True)
                self.scr.hesap_butonu.setVisible(True)


app = QApplication([])
main_form = MainWindow()
main_form.show()
app.exec_()
