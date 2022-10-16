import time
import board
import adafruit_mpu6050
import numpy as np
import matplotlib.pylab as plt

from pathlib import Path

i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_2_G
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_250_DPS

mpu.cycle_Rate = adafruit_mpu6050.Rate.CYCLE_40_HZ
mpu.sleep = True
mpu.cycle = True


recordings = []
for k in range(200):

    recordings.append(
        (time.perf_counter(), *mpu.acceleration)
    )
    print(k)

    # print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.gyro))
    time.sleep(0.020)
    # print("Temperature: %.2f C"%mpu.temperature)
    # print("")
    # time.sleep(1)
    
recordings = np.array(recordings)

plt.plot(recordings[:, 0], recordings[:, 1], label='ax')
plt.plot(recordings[:, 0], recordings[:, 2], label='ay')
plt.plot(recordings[:, 0], recordings[:, 3], label='az')
Path('output').mkdir(parents=True, exist_ok=True)
plt.savefig('output/acc_exy.png')


"""
adafruit_mpu6050: limited to 40Hz ? https://docs.circuitpython.org/projects/mpu6050/en/latest/api.html

Need to use FIFO buffer... (1kHz max on acc data)
https://github.com/jrowberg/i2cdevlib/blob/master/RaspberryPi_bcm2835/MPU6050/examples/IMU_zero.cpp
https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
"""