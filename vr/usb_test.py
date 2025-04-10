import serial
import struct


ser = serial.Serial('/dev/ttyGS0', 115200)
data = struct.pack('fff', 1.23, 4.56, 7.89)
while True:
    ser.write(data)