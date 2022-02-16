from mpu6050 import mpu6050


sensor = mpu6050(0x68)

accelerometer_data = sensor.get_accel_data()

print(accelerometer_data)

print(sensor.get_gyro_data())

print(sensor.get_all_data())

print(sensor.get_temp())

# from smbus import SMBus

# I2C_ADDRESS = 0x68

# TEMP_OUt_ADDR = 0x41

# PWR_MGMT_1 = 0x6B
# i2c = SMBus(1)

# i2c.write_byte_data(I2C_ADDRESS, PWR_MGMT_1, 0x00)

# data = i2c.read_i2c_block_data(
#     I2C_ADDRESS, TEMP_OUt_ADDR, 6
# )

# print(data)


    # note: Doesn't work...
    # def _read(self, register_addr, register_length) -> int:
    #     return self.i2c.read_i2c_block_data(
    #         self.I2C_ADDRESS, register_addr, register_length
    #     )