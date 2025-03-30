import socket
import struct
import time
import board
import busio
import adafruit_bno055

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

IP = "192.168.0.112"
PORT = 6969
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    quat = sensor.quaternion
    if quat is not None:
        qw, qx, qy, qz = quat

        packet = struct.pack("<BBffff", 1, 0, qx, qy, qz, qw)  # <BB = header, ID | ffff = 4 floats

        sock.sendto(packet, (IP, PORT))

    time.sleep(0.01)