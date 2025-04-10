import socket
import time
import board
import busio
import adafruit_bno055
import array

# Set up I2C and the sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Define the IP and port
IP = "hub-us-gw.zcu.cz"  # PC's IP address
PORT = 30022  # The port used for communication

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', PORT))  # Bind the socket to listen on the specified port

while True:
    # Listen for incoming messages
    data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
    print(f"Received message: {data} from {addr}")

    # Check if the message is a valid request (you can define this check based on your needs)
    if data:
        quat = sensor.quaternion
        quat = [quat[1], quat[0], quat[2], quat[3]]  # Reorder quaternion if necessary

        if quat is not None:
            # Convert quaternion to bytes
            packet = array.array('f', quat).tobytes()

            # Send the response back to the PC
            sock.sendto(packet, addr)  # Send data back to the sender's address

    time.sleep(0.01)  # Sleep for a short time to avoid excessive CPU usage