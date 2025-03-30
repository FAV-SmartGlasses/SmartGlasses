import socket
import struct

IP = "0.0.0.0"  # Listen on all available network interfaces
PORT = 6969  # Match the port from SlimeVR

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

print(f"Listening for UDP packets on {PORT}...")

while True:
    data, addr = sock.recvfrom(1024)  # Receive UDP data
    print(f"Received {len(data)} bytes from {addr}: {data}")

    # Try to unpack it using SlimeVR format
    try:
        unpacked = struct.unpack("<BBffff", data)  # Header, Tracker ID, Quaternion (x, y, z, w)
        print(f"Tracker ID: {unpacked[1]}, Quaternion: {unpacked[2:]}")
    except struct.error:
        print("Received data doesn't match expected format!")
