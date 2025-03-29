import time
import board
import busio
import adafruit_bno055
import socket
import json

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

IP = "192.168.0.112"
PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_bno055_data():
    euler = sensor.euler
    if euler is None:
        return

    yaw, roll, pitch = euler

    imu_data = {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
        "yaw": yaw,
        "pitch": pitch,
        "roll": roll
    }

    message = json.dumps(imu_data)
    sock.sendto(message.encode(), (IP, PORT))

try:
    while True:
        send_bno055_data()
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Program terminated.")
    sock.close()