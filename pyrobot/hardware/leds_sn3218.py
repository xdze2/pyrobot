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

        self.gamma_step = [int(255 * (step / 255) ** 1.5) for step in range(256)]

        self.start()
        self.enable_all_leds()

    def set_raw_pwm(self, values: List[int]):
        self._write(self.SET_PWM_REGISTER, values)
        self._update()

    def set_intensity(self, values: List[int]):
        """Apply gamma correction."""
        raw_values = [self._gamma(step) for step in values]
        self.set_raw_pwm(raw_values)

    def _write(self, register_addr, data: List[int]):
        self.i2c.write_i2c_block_data(self.I2C_ADDRESS, register_addr, data)

    # def hardware_shutdown(self):
    #     gpio.write(self.UNDERLIGHTING_EN_PIN, 1)

    # note: Doesn't work...
    # def _read(self, register_addr, register_length) -> int:
    #     return self.i2c.read_i2c_block_data(
    #         self.I2C_ADDRESS, register_addr, register_length
    #     )

    def start(self):
        """Normal operation."""
        self._write(
            self.SHUTDOWN_REGISTER,
            [0x01],
        )

    def shutdown(self):
        """Software shutdown mode."""
        self._write(
            self.SHUTDOWN_REGISTER,
            [0x00],
        )

    def _update(self):
        """Update new state of Ctrl and PWM registers."""
        self._write(
            self.UPDATE_REGISTER,
            [0xFF],
        )

    def enable_all_leds(self):
        enable_mask = 0b111_111_111_111_111_111
        self._write(
            self.LED_CTRL_REGISTER,
            [enable_mask & 0x3F, (enable_mask >> 6) & 0x3F, (enable_mask >> 12) & 0x3F],
        )
        self._update()

    def _gamma(self, step: int):
        return self.gamma_step[min(255, step)]
