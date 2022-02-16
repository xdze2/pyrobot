
import time

from typing import List


import pigpio
from smbus import SMBus


class SN3218:

    SHUTDOWN_REGISTER = 0x00
    SET_PWM_REGISTER = 0x01
    LED_CTRL_REGISTER = 0x13
    UPDATE_REGISTER = 0x16
    RESET_REGISTER = 0x17
    
    I2C_ADDRESS = 0x54

    def __init__(self):
        
        self.UNDERLIGHTING_EN_PIN = 7

        gpio = pigpio.pi()
        gpio.set_mode(self.UNDERLIGHTING_EN_PIN, pigpio.OUTPUT)
        gpio.write(self.UNDERLIGHTING_EN_PIN, 1)

        self.i2c = SMBus(1)

        self.start()
        self.enable_all_leds()

    # def hardware_shutdown(self):
    #     gpio.write(self.UNDERLIGHTING_EN_PIN, 1)  

    def _write(self, register_addr, data: List[int]):
        self.i2c.write_i2c_block_data(self.I2C_ADDRESS, register_addr, data)

    def start(self):
        """Normal operation."""
        self._write(self.SHUTDOWN_REGISTER, [0x01, ])

    def shutdown(self):
        """Software shutdown mode."""
        self._write(self.SHUTDOWN_REGISTER, [0x00, ])

    def _update(self):
        """Update new state of Ctrl and PWM registers."""
        self._write(self.UPDATE_REGISTER, [0xFF, ])

    def enable_all_leds(self):
        enable_mask = 0b111_111_111_111_111_111
        self._write(
            self.LED_CTRL_REGISTER,
            [enable_mask & 0x3F, (enable_mask >> 6) & 0x3F, (enable_mask >> 12) & 0x3F],
        )
        self._update()    

    def set_raw_pwm(self, values: List[int]):
        self._write(
            self.SET_PWM_REGISTER,
            values
        )
        self._update()


sn = SN3218()

values = [
    250, 0, 250,
    250, 250, 0,
    250, 0, 250,
    250, 250, 0,
    250, 0, 250,
    1, 250, 0,
]

sn.set_raw_pwm(values)

for k in range(10):
    sn.start()
    time.sleep(0.5)
    sn.shutdown()
    time.sleep(0.5)
# default_gamma_table = [int(pow(255, float(i - 1) / 255)) for i in range(256)]
# print(default_gamma_table)
# channel_gamma_table = [default_gamma_table for _ in range(18)]

# i2c.write_i2c_block_data(I2C_ADDRESS, CMD_SET_PWM_VALUES, [channel_gamma_table[i][values[i]] for i in range(18)])
# i2c.write_i2c_block_data(I2C_ADDRESS, CMD_UPDATE, [0xFF])



# time.sleep(1)
