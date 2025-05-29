import socket
import time
import board
import busio
import adafruit_bno055  # pip install adafruit-circuitpython-bno055
import array
    
# Define IP and port
IP = "0.0.0.0"  # Listen on all interfaces
PORT = 31000

class SteamVR_IMU_manager:   
    def __init__(self):
        # Set up I2C and the sensor
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)

        # Create a TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(1)

        print(f"Server ready on port {PORT}...")

    def send_imu_data(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Client connected from {client_address}")

                with client_socket:
                    try:
                        while True:
                            quat = self.sensor.quaternion
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
            self.server_socket.close()
