from mpu6050 import mpu6050
import time

imu = mpu6050(0x68)


imu.set_accel_range(mpu6050.ACCEL_RANGE_2G)

# print(imu.get_accel_data())
# print(imu.get_gyro_data())
# print(imu.get_all_data())
# print(imu.get_temp())


def format_vector(vector):
    return ' '.join((f'{v: 8.3f}{k}' for k, v  in vector.items()))

while True:
    acc, gyro, T = imu.get_all_data()
    print(f"{time.time(): 10f}", format_vector(acc), format_vector(gyro))
    time.sleep(0.5)