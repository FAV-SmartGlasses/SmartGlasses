import socket
import time
import board
import busio
import adafruit_bno055
import array

IP = "0.0.0.0"
PORT = 31000

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

def try_connect_sensor(i2c, attempts=10, delay=0.5):
    for _ in range(attempts):
        try:
            sensor = adafruit_bno055.BNO055_I2C(i2c)
            if sensor.quaternion is not None:
                print("Sensor connected.")
                return sensor
        except:
            pass
        time.sleep(delay)
    return None

def wait_for_valid_quat(sensor, timeout=3.0):
    start = time.time()
    while time.time() - start < timeout:
        q = sensor.quaternion
        if q is not None:
            return reorder_bno(q)
        time.sleep(0.1)
    return None

def reorder_bno(q):  # (w, x, y, z) › (x, y, z, -w)
    return [q[1], q[0], q[2], -q[3]]

def quat_inverse(q):
    x, y, z, w = q
    return [-x, -y, -z, w]

def quat_multiply(q1, q2):
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    return [
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
        w1*w2 - x1*x2 - y1*y2 - z1*z2
    ]

def main():
    sensor = try_connect_sensor(i2c)
    if not sensor:
        print("Could not connect to BNO055.")
        return

    zero_quat = wait_for_valid_quat(sensor)
    if not zero_quat:
        print("Failed to get initial orientation.")
        return
    print("Initial orientation zeroed.")

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
                        q = sensor.quaternion
                        if q is None:
                            continue

                        q_now = reorder_bno(q)
                        q_rel = quat_multiply(quat_inverse(zero_quat), q_now)

                        packet = array.array('f', q_rel).tobytes()
                        client_socket.sendall(packet)

                        time.sleep(0.01)  # ~100 Hz
                    except (ConnectionResetError, BrokenPipeError):
                        print("Client disconnected.")
                        break
                    except OSError as e:
                        print(f"Sensor error: {e}. Reconnecting...")
                        sensor = try_connect_sensor(i2c)
                        if not sensor:
                            break
                        zero_quat = wait_for_valid_quat(sensor)
                        if not zero_quat:
                            print("Failed to re-zero sensor.")
                            break
                        print("Sensor reconnected and zeroed.")

try:
    main()
except KeyboardInterrupt:
    print("Exiting cleanly.")
