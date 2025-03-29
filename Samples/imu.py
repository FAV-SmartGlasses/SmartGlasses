import time
import board
import busio
import adafruit_bno055

# Initialize I2C communication
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Function to display sensor readings
def read_bno055():
    print("Temperature: {}°C".format(sensor.temperature))
    print("Accelerometer (m/s²): {}".format(sensor.acceleration))
    print("Gyroscope (deg/s): {}".format(sensor.gyro))
    print("Magnetometer (µT): {}".format(sensor.magnetic))
    print("Euler Angles (°): {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Linear Acceleration (m/s²): {}".format(sensor.linear_acceleration))
    print("Gravity (m/s²): {}".format(sensor.gravity))
    print("-" * 40)

# Read and print data every second
try:
    while True:
        read_bno055()
        time.sleep(1)  # Wait for 1 second before next read
except KeyboardInterrupt:
    print("Program terminated.")