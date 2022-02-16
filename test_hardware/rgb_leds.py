import sn3218 as sn
import time

# leds = sn.SN3218()

# print(sn.__version__)
# enable_mask = 0b111111100011111111
# leds.enable_leds(enable_mask)
#

import pigpio
from smbus import SMBus

UNDERLIGHTING_EN_PIN = 7

gpio = pigpio.pi()
gpio.set_mode(UNDERLIGHTING_EN_PIN, pigpio.OUTPUT)
gpio.write(UNDERLIGHTING_EN_PIN, 1)


I2C_ADDRESS = 0x54
CMD_ENABLE_OUTPUT = 0x00
CMD_SET_PWM_VALUES = 0x01
CMD_ENABLE_LEDS = 0x13
CMD_UPDATE = 0x16
CMD_RESET = 0x17


i2c = SMBus(1)

print(i2c)

# enable
i2c.write_i2c_block_data(I2C_ADDRESS, CMD_ENABLE_OUTPUT, [0x01])


enable_mask = 0b111_111_111_111_111_111
i2c.write_i2c_block_data(
    I2C_ADDRESS,
    CMD_ENABLE_LEDS,
    [enable_mask & 0x3F, (enable_mask >> 6) & 0x3F, (enable_mask >> 12) & 0x3F],
)
time.sleep(1)
i2c.write_i2c_block_data(I2C_ADDRESS, CMD_UPDATE, [0xFF])


values = [
    1, 0, 1,
    1, 1, 0,
    1, 0, 1,
    1, 1, 0,
    1, 0, 1,
    1, 0,0 ,
]


default_gamma_table = [int(pow(255, float(i - 1) / 255)) for i in range(256)]
channel_gamma_table = [default_gamma_table for _ in range(18)]

i2c.write_i2c_block_data(I2C_ADDRESS, CMD_SET_PWM_VALUES, [channel_gamma_table[i][values[i]] for i in range(18)])
i2c.write_i2c_block_data(I2C_ADDRESS, CMD_UPDATE, [0xFF])



time.sleep(1)
