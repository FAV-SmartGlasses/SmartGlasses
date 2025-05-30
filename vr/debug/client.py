import socket
import array

# Server details
SERVER_IP = "192.168.0.121"  # Replace with your server's IP
PORT = 31000

# Create TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((SERVER_IP, PORT))

    while True:
        # Receive 16 bytes (4 floats, 4 bytes each)
        data = sock.recv(16)

        # Convert bytes to 4 float values
        quat = array.array('f')
        quat.frombytes(data)

        print("Received quaternion:", list(quat))