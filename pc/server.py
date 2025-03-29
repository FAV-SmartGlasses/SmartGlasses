import socket
import struct

PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("Listening for IMU data...")

while True:
    data, _ = sock.recvfrom(1024)
    yaw, roll, pitch = struct.unpack("fff", data)
    print(f"Yaw: {yaw:.2f}, Roll: {roll:.2f}, Pitch: {pitch:.2f}")