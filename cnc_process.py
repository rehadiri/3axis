from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import time
import serial

z_cut_pos = 5

class cnc_processing(QWidget):
    def __init__(self, rectangles):
        super().__init__()
        self.rectangles = rectangles
        self.start_cutting()

    def initialize_serial(self):
        ser = serial.Serial(port='COM3', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        time.sleep(2)
        return ser

    def wake_up_grbl(self, s):
        # Wake up CNC grbl
        s.write(str.encode("\r\n\r\n"))
        time.sleep(2)  # Wait for initialization
        s.flushInput()  # Flush startup text in serial input

    def unlock(self, s):
        unlock = "$X"
        unlock.strip()
        s.write(str.encode(unlock) + str.encode('\n'))
        grbl_out = s.readline()
        print(grbl_out.strip().decode("utf-8"))
        grbl_out = s.readline()
        print(grbl_out.strip().decode("utf-8"))

    def send_gcode(self, s, g_code):
        g_code.strip()
        s.write(str.encode(g_code) + str.encode('\n'))
        response = ""
        while response.strip() != "ok":
            grbl_out = s.readline()
            response = grbl_out.decode("utf-8")
            print(response)

    def cut_single_rect(self, ser, x1, y1, x2, y2):
        start_pos = "G00 " + "X" + str(x1) + " Y" + str(y1) + " Z5 \n"  # dikdörtgen köşesine git
        start_pos = start_pos +"G92 "
        self.send_gcode(ser, start_pos)
        time.sleep(0.5)
        x2 += x1
        y2 += y1
        cut_code = "M3 S255 \n"
        cut_code = cut_code + "G01 " + "X" + str(x2) + " Y" + str(y1) + " Z" + str(z_cut_pos) + " F100 \n"
        cut_code = cut_code + "G01 " + "X" + str(x2) + " Y" + str(y2) + " Z" + str(z_cut_pos) + " F100 \n"
        cut_code = cut_code + "G01 " + "X" + str(x1) + " Y" + str(y2) + " Z" + str(z_cut_pos) + " F100 \n"
        cut_code = cut_code + "G01 " + "X" + str(x1) + " Y" + str(y1) + " Z" + str(z_cut_pos) + " F100 \nM5"
        print(cut_code)
        self.send_gcode(ser, cut_code)
        time.sleep(0.5)

    def start_cutting(self):
        msgtext = " CNC bağlı ve kesmeye hazır durumda mı ?"
        ret = QMessageBox.question(self, " CNC Kontrol ", msgtext, QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            ser = self.initialize_serial()
            self.wake_up_grbl(ser)
            time.sleep(1)

            self.unlock(ser)
            time.sleep(1)

            code1 = "$H"  # homing cycle
            self.send_gcode(ser, code1)

            time.sleep(1)
            print(" home cycle ends ")

            init_pos = "G92 X00 Y00 Z00"  # Set Origin
            self.send_gcode(ser, init_pos)
            time.sleep(1)

            for rectangle in self.rectangles:
                print(rectangle)
                self.cut_single_rect(ser, rectangle[0], rectangle[1], rectangle[2], rectangle[3])

            code1 = "?"  # Staus report
            self.send_gcode(ser, code1)
            time.sleep(1)

            ser.close()
