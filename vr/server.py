import socket
import time
import board
import busio
import adafruit_bno055  # pip install adafruit-circuitpython-bno055
import array

# Set up I2C and the sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Define IP and port
IP = "0.0.0.0"  # Listen on all interfaces
PORT = 31000

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(1)

print(f"Server ready on port {PORT}...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected from {client_address}")

        with client_socket:
            try:
                while True:
                    quat = sensor.quaternion
                    if quat is not None:
                        quat = [quat[1], quat[0], quat[2], -quat[3]]  # Reorder if needed
                        packet = array.array('f', quat).tobytes()
                        client_socket.sendall(packet)

                    time.sleep(0.01)  # 100 Hz update rate
            except ConnectionResetError or BrokenPipeError:
                print("Client disconnected unexpectedly.")

        print("Client disconnected.")

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    server_socket.close()
