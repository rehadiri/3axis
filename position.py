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
    grbl_out = s.readline()
    print(grbl_out.strip().decode("utf-8"))


ser = initialize_serial()
wake_up_grbl(ser)
print("Wake up grbl")

time.sleep(1)

unlock(ser)
time.sleep(1)

code1 = "G90"  # Absolute positioning
send_gcode(ser, code1)
time.sleep(0.5)

code1 = "G01 X10 Y00 Z02 F100"  # go to x 100mm/sec cutting speed
send_gcode(ser, code1)
time.sleep(0.5)

code1 = "G00 X00 Y00 Z00"  # go to x y locate fast
send_gcode(ser, code1)
time.sleep(0.5)

code1 = "G01 X20 Y00 Z02 F100"  # go to x 100mm/sec
send_gcode(ser, code1)
time.sleep(0.5)

code1 = "G00 X00 Y00 Z00 "  # go to x y
send_gcode(ser, code1)
time.sleep(0.5)

# code1 = "G00 X00 Y00 Z00"  # return to start position
# send_gcode(ser, code1)
# mcode = "M05" # stop spindle
# send_gcode(ser, mcode)
# time.sleep(1)

time.sleep(3)
ser.close()
