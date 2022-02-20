import time

from typing import List


from pyrobot.hardware.leds_sn3218 import SN3218

sn = SN3218()

values = [
    250,
    0,
    250,
    250,
    250,
    0,
    250,
    0,
    250,
    250,
    250,
    0,
    250,
    0,
    250,
    1,
    250,
    0,
]

# sn.set_raw_pwm(values)

for uu in range(10):
    for k in range(256):
        values = [k]*18
        sn.set_pwm(values)
        time.sleep(.00005)

    for k in range(0, 240, 2):
        values = [255 - k]*18
        sn.set_pwm(values)
        time.sleep(.001)

    break

# sn.shutdown()
# default_gamma_table = [int(pow(255, float(i - 1) / 255)) for i in range(256)]
# print(default_gamma_table)
# channel_gamma_table = [default_gamma_table for _ in range(18)]

# i2c.write_i2c_block_data(I2C_ADDRESS, CMD_SET_PWM_VALUES, [channel_gamma_table[i][values[i]] for i in range(18)])
# i2c.write_i2c_block_data(I2C_ADDRESS, CMD_UPDATE, [0xFF])


# time.sleep(1)
