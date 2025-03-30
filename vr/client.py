import socket
import struct
import time
import board
import busio
import adafruit_bno055

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

IP = "192.168.0.112"
PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    euler = sensor.euler
    if euler is not None:
        yaw, roll, pitch = euler

        data = struct.pack("fff", yaw or 0.0, pitch or 0.0, roll or 0.0)
        sock.sendto(data, (IP, PORT))
    time.sleep(0.01)