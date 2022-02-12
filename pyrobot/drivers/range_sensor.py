
import time
import pigpio

gpio = pigpio.pi()


import numpy as np

class UltraSoundSensor:

    def __init__(self, gpio_trig: int, gpio_echo: int):
        self.echo_pin = gpio_echo
        self.trig_pin = gpio_trig

        gpio.set_mode(self.trig_pin, pigpio.OUTPUT)
        gpio.set_mode(self.echo_pin, pigpio.INPUT)

        self.cm_per_us = +0.0177909
        self.offset_cm = -1.6430462

    def _callback_rising(self, _gpio_id: int, _value: bool, tick: int):
        self.tic = tick

    def _callback_falling(self, _gpio_id: int, _value: bool, tick: int):
        self.toc = tick

    def measure_us(self) -> int:
        """Get total echo time in micro-second."""
        self.tic = None
        self.toc = None

        e1 = gpio.callback(self.echo_pin, pigpio.RISING_EDGE, self._callback_rising)
        e2 = gpio.callback(self.echo_pin, pigpio.FALLING_EDGE, self._callback_falling)
        
        gpio.gpio_trigger(self.trig_pin, 12, 1)  # 10 us

        for _ in range(10):
            if self.tic is not None and self.toc is not None:
                e1.cancel()
                e2.cancel()
                return self.toc - self.tic
            else:
                time.sleep(.005)
        else:
            e1.cancel()
            e2.cancel()
            raise TimeoutError

    def measure_cm(self, nbr_measure: int=3) -> float:
        echo_time = np.mean([self.measure_us() for _ in range(nbr_measure)])
        return round( echo_time * self.cm_per_us + self.offset_cm )

    @staticmethod
    def calib():
        cm_per_us, offset_cm = np.polyfit(
            calib_cm_us[:, 1],
            calib_cm_us[:, 0], 
            deg=1
        )



# HC-SR04 Ultrasound pins
ULTRA_TRIG_PIN = 13
ULTRA_ECHO_PIN = 25

sensor = UltraSoundSensor(gpio_echo=ULTRA_ECHO_PIN, gpio_trig=ULTRA_TRIG_PIN)

# calib_cm_us = np.array([
#     [10, 658],
#     [20, 1210],
#     [30, 1773],
#     [40, 2358],
#     [50, 2894]
# ])



print(sensor.measure_cm())