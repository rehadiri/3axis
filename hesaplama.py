import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from hesap_ui import Ui_hesap_widget
from cnc_process import cnc_processing
import sys


class hesapla(QWidget):
    def __init__(self, main_windows_pos, rectangles, tezgah_boy, tezgah_en):
        # Setting up the widgets and layout
        super().__init__()
        self.scr = Ui_hesap_widget()
        self.scr.setupUi(self)
        new_pos = main_windows_pos + QtCore.QPoint(30, 100)
        self.move(new_pos)
        self.scr.exit_butonu.clicked.connect(self.exit_form)
        self.tezgah_en = tezgah_en
        self.tezgah_boy = tezgah_boy
        self.altlik = np.zeros(shape=(tezgah_boy, tezgah_en), dtype=np.uint8)
        self.uygun_yer = []
        self.display_final_rects = []
        self.rect_labels = []
        self.rectangles = self.extend_rectangles(rectangles)
        self.sorted_rects = self.sort_rectangles(self.rectangles)
        self.optimizasyon()
        self.cnc_obj = None
        self.scr.cnc_butonu.clicked.connect(self.cnc_process)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
        for display_rectangle in self.display_final_rects:
            x1 = display_rectangle[0]
            y1 = display_rectangle[1]
            x2 = display_rectangle[2]
            y2 = display_rectangle[3]
            qp.drawRect(x1, y1, x2, y2)

    def exit_form(self):
        self.close()

    def cnc_process(self):
        cut_rectangles = []
        for cut_rect in self.sorted_rects:
            cut_rectangles.append([cut_rect[2],cut_rect[3],cut_rect[0],cut_rect[1]])
        if self.cnc_obj is not None:
            del self.cnc_obj
        self.cnc_obj = cnc_processing(cut_rectangles)

    def extend_rectangles(self, rectangles):
        extended_rects = []
        index = 0
        for rects in rectangles:
            en = rects[0]
            boy = rects[1]
            # rectangles listesinde 3,4 kolonlar yerleştirilme sonrası yerleşme koordinatı olacak
            # rectangles listesinde 5. kolon dikdörtgen alanıdır, sort ederken kullanılır.
            # rectangles listesinde 6. kolon dikdörtgenin index no.
            index += 1
            extended_rects.append([en, boy, -1, -1, (en * boy), index])
        return extended_rects

    def sort_rectangles(self, rectangles):
        return sorted(rectangles, key=lambda rectangles: rectangles[4], reverse=True)

    def alan_hesapla(self):
        # Dikdörtgen yerleştirildiğinde Kullanılacak toplam alan hesaplanır
        max_x = 0
        max_y = 0
        for located_rect in self.sorted_rects:
            if located_rect[2] != -1 and located_rect[3] != -1:
                if (located_rect[0] + located_rect[2]) > max_x:
                    max_x = located_rect[0] + located_rect[2]
                if (located_rect[1] + located_rect[3]) > max_y:
                    max_y = located_rect[1] + located_rect[3]
        return max_x * max_y

    def yer_kontrol_loop(self, index, boy, en, min_alan, rotated):
        pos = 0
        if rotated:
            en, boy = boy, en
        for i in range(len(self.uygun_yer)):
            # print('uygun yerler : ',self.uygun_yer)
            yer = self.uygun_yer[i]
            yer_x = yer[0]
            yer_y = yer[1]
            yer_free = yer[2]
            # yerleştirilecek alan tamamen boş mu ve diğer kontroller
            all_zeros = not np.any(self.altlik[yer_x:yer_x + boy, yer_y:yer_y + en])
            if all_zeros and yer_free and yer_x + boy < self.tezgah_boy \
                    and yer_y + en < self.tezgah_en:
                # dikdörtgen geçici olarak konumlanır
                self.sorted_rects[index] = [boy, en, yer_x, yer_y, (en * boy), 0]
                # toplam alan kontrol edilir
                alan = self.alan_hesapla()
                if alan < min_alan:
                    min_alan = alan
                    pos = i
        print('Alan :', min_alan, ' Rotated :', rotated)
        return pos, min_alan

    def yerlestirme(self, index):
        rectangle = self.sorted_rects[index]
        boy = rectangle[0]
        en = rectangle[1]
        rect_no = rectangle[5]
        pos1, min_alan1 = self.yer_kontrol_loop(index, boy, en, sys.maxsize, False)
        pos2, min_alan2 = self.yer_kontrol_loop(index, boy, en, sys.maxsize, True)
        # Dikdörgenin yerleştirip yerleştirilemediği kontrol edilir,
        # Dikdörtgen yerleştirilemiyorsa fonksiyon False döner
        rectangle = self.sorted_rects[index]
        if rectangle[5] == 0:  # Dikdörtgen yerleştirilmişse
            if min_alan2 < min_alan1:
                en, boy = boy, en
                pos = pos2
            else:
                pos = pos1
            # en uygun yer False set edilerek listeden çıkartılır
            yer = self.uygun_yer[pos]
            yer_x = yer[0]
            yer_y = yer[1]
            self.uygun_yer[pos] = [yer_x, yer_y, False]
            # altlıkta bu alan kullanılmış olarak set edilir
            self.altlik[yer_x:yer_x + boy, yer_y:yer_y + en] = 1
            # dikdörtgenin için en uygun yer dikdörtgene atanır
            self.sorted_rects[index] = [boy, en, yer_x, yer_y, (en * boy), rect_no]
            # Yeni uygun yerler listeye eklenir
            xx = yer_x + boy
            yy = yer_y
            while True:
                if yy <= 0 or self.altlik[xx][yy] != 0:
                    break
                yy = yy - 1
            if self.altlik[xx][yy] != 0:
                yy += 1
            self.uygun_yer.append([xx, yy, True])
            yy = yer_y + en
            xx = yer_x
            while True:
                if xx <= 0 or self.altlik[xx][yy] != 0:
                    break
                xx = xx - 1
            if self.altlik[xx][yy] != 0:
                xx += 1
            self.uygun_yer.append([xx, yy, True])
            print('uygun yer append sonrası : ', self.uygun_yer)

            # yerleştirme yapıldıktan sonra geri dönülür
            return True
        else:
            return False # Dikdörtgen hiçbir şekilde yerleşmedi

    def optimizasyon(self):

        print(self.sorted_rects)
        self.uygun_yer.clear()
        # uygun_yer kolonları : en , boy , kullanıma uygunluk
        self.uygun_yer.append([0, 0, True])

        for i in range(len(self.sorted_rects)):
            yerlesme_flag = self.yerlestirme(i)
            if not yerlesme_flag:
                QMessageBox.about(self, "Hata", "Tüm Dikdörtgenler Yerleştirilememiştir ! ")
                break

        if yerlesme_flag:
            print('Result : ', self.sorted_rects)
            # Dikdörtgenlerin ekranda gösterilmesi
            base_x = 100
            base_y = 350
            for rectangle in self.sorted_rects:
                x1 = base_x + (rectangle[2] * 2)
                y1 = base_y - (rectangle[3] * 2) - (rectangle[1] * 2)
                x2 = (rectangle[0] * 2) + 1
                y2 = (rectangle[1] * 2)
                print(x1, y1, x2, y2)
                self.display_final_rects.append([x1, y1, x2, y2])
                self.rect_labels.append(QtWidgets.QLabel(self))
                self.rect_labels[-1].setGeometry(QtCore.QRect(x1, y1, x2, y2))
                self.rect_labels[-1].setAlignment(QtCore.Qt.AlignCenter)
                self.rect_labels[-1].setText(str(rectangle[5]))
            self.update()
            for labels in self.rect_labels:
                labels.show()
            toplam_alan = self.alan_hesapla()
            self.scr.alan.setText("Kullanılan Alan : " + str(toplam_alan) + " m2")
            self.show()

    def close_widget(self):
        self.close()
