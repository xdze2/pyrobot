import time
import board
import adafruit_mpu6050


class Imu:
    def __init__(self, buffer):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.mpu = adafruit_mpu6050.MPU6050(i2c)
        self.run = True
        self.data = buffer

    def get_gyro(self):
        return self.mpu.gyro

    def loop(self):

        while self.run:
            self.data.append(self.get_gyro())
            time.sleep(0.001)

        print("Stop recording", len(self.data))


# while True:

#     print(f"{time.perf_counter():.3f}", "Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.acceleration))

#     # print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.gyro))
#     time.sleep(0.02)
#     # print("Temperature: %.2f C"%mpu.temperature)
#     # print("")
#     # time.sleep(1)

#     break
