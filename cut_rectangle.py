import time
import serial

cut_pos = 5


def initialize_serial():
    ser = serial.Serial(port='COM3', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    time.sleep(2)
    return ser


def wake_up_grbl(s):
    # Wake up CNC grbl
    s.write(str.encode("\r\n\r\n"))
    time.sleep(2)  # Wait for initialization
    s.flushInput()  # Flush startup text in serial input


def unlock(s):
    unlock = "$X"
    unlock.strip()
    s.write(str.encode(unlock) + str.encode('\n'))
    grbl_out = s.readline()
    print(grbl_out.strip().decode("utf-8"))
    grbl_out = s.readline()
    print(grbl_out.strip().decode("utf-8"))


def send_gcode(s, g_code):
    g_code.strip()
    s.write(str.encode(g_code) + str.encode('\n'))
    response = ""
    while response.strip() != "ok":
        grbl_out = s.readline()
        response = grbl_out.decode("utf-8")
        print(response)


def cut_single_rect(x1, y1, x2, y2):

    start_pos = "G00 " + "X" + str(x1) + " Y" + str(y1) + " Z5 \n"  # dikdörtgen köşesine git
    send_gcode(ser, start_pos)
    time.sleep(0.5)

    x2 += x1
    y2 += y1

    cut_code = "M3 S255 \n"
    cut_code = cut_code + "G01 " + "X" + str(x2) + " Y" + str(y1) + " Z" + str(cut_pos) + " F100 \n"
    cut_code = cut_code + "G01 " + "X" + str(x2) + " Y" + str(y2) + " Z" + str(cut_pos) + " F100 \n"
    cut_code = cut_code + "G01 " + "X" + str(x1) + " Y" + str(y2) + " Z" + str(cut_pos) + " F100 \n"
    cut_code = cut_code + "G01 " + "X" + str(x1) + " Y" + str(y1) + " Z" + str(cut_pos) + " F100 \nM5"
    print(cut_code)
    send_gcode(ser, cut_code)
    time.sleep(0.5)


rect_list = []

ser = initialize_serial()

wake_up_grbl(ser)
time.sleep(1)

unlock(ser)
time.sleep(1)

code1 = "$H"  # homing cycle
send_gcode(ser, code1)
time.sleep(1)
print(" home cycle ends ")

init_origin = "G92 X00 Y00 Z00 \n"  # Init Origin
send_gcode(ser, init_origin)
time.sleep(0.5)

rect_list.append([0, 0, 10, 10])
rect_list.append([10, 0, 10, 10])


for rectangle in rect_list:
    cut_single_rect(rectangle[0], rectangle[1], rectangle[2], rectangle[3])

code1 = "?"  # Staus report
send_gcode(ser, code1)
time.sleep(1)

ser.close()
