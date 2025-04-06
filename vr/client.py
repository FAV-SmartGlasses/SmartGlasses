import socket
import time
import board
import busio
import adafruit_bno055
import array

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

IP = "192.168.0.112"
PORT = 6969
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    quat = sensor.quaternion
    quat = [quat[1], quat[0], quat[2], quat[3]]
    if quat is not None:
        # Just pack the 4 floats: qw, qx, qy, qz (or whatever order you prefer)
        packet = array.array('f', quat).tobytes()
        sock.sendto(packet, (IP, PORT))

    time.sleep(0.01)