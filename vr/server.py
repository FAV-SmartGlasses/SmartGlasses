import socket
import time
import board
import busio
import adafruit_bno055  # pip install adafruit-circuitpython-bno055
import array

# Define IP and port
IP = "0.0.0.0"
PORT = 31000

# Set up I2C outside the loop so it persists across reconnects
i2c = busio.I2C(board.SCL, board.SDA)

def try_connect_sensor(i2c, attempts=10, delay=0.5):
    """Try to connect to the BNO055 sensor with retries."""
    for attempt in range(attempts):
        try:
            sensor = adafruit_bno055.BNO055_I2C(i2c)
            if sensor.quaternion is not None:
                print("Sensor connected.")
                return sensor
        except Exception as e:
            print(f"Sensor connect attempt {attempt+1} failed: {e}")
        time.sleep(delay)
    return None

def main():
    sensor = try_connect_sensor(i2c)
    if not sensor:
        print("Could not connect to BNO055 sensor. Exiting.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((IP, PORT))
        server_socket.listen(1)
        print(f"Server ready on port {PORT}...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}")

            with client_socket:
                while True:
                    try:
                        quat = sensor.quaternion
                        if quat is None:
                            continue

                        quat = [quat[1], quat[0], quat[2], -quat[3]]
                        packet = array.array('f', quat).tobytes()
                        client_socket.sendall(packet)

                        time.sleep(0.01)  # ~100Hz
                    except (ConnectionResetError, BrokenPipeError):
                        print("Client disconnected unexpectedly.")
                        break
                    except OSError as e:
                        print(f"Sensor error: {e}. Attempting to reconnect...")
                        sensor = try_connect_sensor(i2c)
                        if not sensor:
                            print("Failed to reconnect to sensor. Closing client connection.")
                            break

            print("Client disconnected.")

try:
    main()
except KeyboardInterrupt:
    print("\nShutting down gracefully.")
