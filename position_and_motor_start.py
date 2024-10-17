import time
import serial


def initialize_serial():
    ser = serial.Serial(port='COM3', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    time.sleep(2)
    return ser


def wake_up_grbl(s):
    # Wake up CNC grbl
    s.write(str.encode("\r\n\r\n"))
    time.sleep(2)  # Wait for initialization
    s.flushInput()  # Flush startup text in serial input


def send_gcode(s, g_code):
    g_code.strip()
    s.write(str.encode(g_code) + str.encode('\n'))
    grbl_out = s.readline()
    print(grbl_out.strip().decode("utf-8"))


ser = initialize_serial()
wake_up_grbl(ser)

time.sleep(1)

code1 = "$X"  # unlock
send_gcode(ser, code1)
time.sleep(0.5)

code1 = "$H"  # set for home
send_gcode(ser, code1)
time.sleep(0.5)

code1 = "G00 X15 Y15 Z05"  # go to x5 y5
send_gcode(ser, code1)
mcode = "M03 S1000" # start spindle with 1000rpm
send_gcode(ser, mcode)
time.sleep(3)

code1 = "G00 X00 Y00 Z00"  # return to start position
send_gcode(ser, code1)
mcode = "M05" # stop spindle
send_gcode(ser, mcode)
time.sleep(1)

