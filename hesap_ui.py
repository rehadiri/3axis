# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hesap.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_hesap_widget(object):
    def setupUi(self, hesap_widget):
        hesap_widget.setObjectName("hesap_widget")
        hesap_widget.resize(800, 500)
        font = QtGui.QFont()
        font.setPointSize(8)
        hesap_widget.setFont(font)
        self.label = QtWidgets.QLabel(hesap_widget)
        self.label.setGeometry(QtCore.QRect(110, 10, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.exit_butonu = QtWidgets.QPushButton(hesap_widget)
        self.exit_butonu.setGeometry(QtCore.QRect(630, 440, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.exit_butonu.setFont(font)
        self.exit_butonu.setObjectName("exit_butonu")
        self.cnc_butonu = QtWidgets.QPushButton(hesap_widget)
        self.cnc_butonu.setGeometry(QtCore.QRect(50, 440, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.cnc_butonu.setFont(font)
        self.cnc_butonu.setObjectName("cnc_butonu")
        self.alan = QtWidgets.QLabel(hesap_widget)
        self.alan.setGeometry(QtCore.QRect(230, 440, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.alan.setFont(font)
        self.alan.setAlignment(QtCore.Qt.AlignCenter)
        self.alan.setObjectName("alan")

        self.retranslateUi(hesap_widget)
        QtCore.QMetaObject.connectSlotsByName(hesap_widget)

    def retranslateUi(self, hesap_widget):
        _translate = QtCore.QCoreApplication.translate
        hesap_widget.setWindowTitle(_translate("hesap_widget", "Hesaplama"))
        self.label.setText(_translate("hesap_widget", "OPTİMİZASYON SONUCU DURUM"))
        self.exit_butonu.setText(_translate("hesap_widget", "ÇIKIŞ"))
        self.cnc_butonu.setText(_translate("hesap_widget", "CNC Process"))
        self.alan.setText(_translate("hesap_widget", "KULLANILAN ALAN :"))
