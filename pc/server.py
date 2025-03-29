import socket
import struct

UDP_PORT = 5555  # Make sure this matches your Pi script
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))

print(f"Listening on port {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)  # Receive data
    print(f"Received {len(data)} bytes: {data}")  # Debug print

    if len(data) == 12:  # Only unpack if we got exactly 12 bytes
        yaw, roll, pitch = struct.unpack("fff", data)
        print(f"Yaw={yaw:.2f}, Roll={roll:.2f}, Pitch={pitch:.2f}")
    else:
        print("Warning: Received unexpected data size!")
