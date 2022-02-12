
import time
import pigpio
import numpy as np


class UltraSoundSensor:
    """Measure distance. Use the pigpio library.
    
    see https://abyz.me.uk/rpi/pigpio/examples.html
    python Sonar Ranger example
    """
    def __init__(self, gpio_trig: int, gpio_echo: int, gpio: pigpio.pi):
        self.echo_pin = gpio_echo
        self.trig_pin = gpio_trig
        self.gpio = gpio

        self.gpio.set_mode(self.trig_pin, pigpio.OUTPUT)
        self.gpio.set_mode(self.echo_pin, pigpio.INPUT)

        # to init, not sure if really needed
        self.gpio.write(self.trig_pin, 0)
        time.sleep(0.01)
        self.gpio.gpio_trigger(self.trig_pin, 15, 1)
        time.sleep(0.01)

        self.cm_per_us = +0.0177909
        self.offset_cm = -1.6430462

    def measure_us(self) -> int:
        """Get total echo time in micro-seconds."""
        self.tic = None
        self.toc = None

        e1 = self.gpio.callback(self.echo_pin, pigpio.RISING_EDGE, self._callback_rising)
        e2 = self.gpio.callback(self.echo_pin, pigpio.FALLING_EDGE, self._callback_falling)
        
        self.gpio.gpio_trigger(self.trig_pin, 15, 1)  # minimum 10 µs

        for _ in range(50):
            if self.tic is not None and self.toc is not None:
                e1.cancel()
                e2.cancel()
                return self.toc - self.tic
            else:
                time.sleep(.0001)
        else:
            e1.cancel()
            e2.cancel()
            raise TimeoutError

    def measure_cm(self, nbr_measure: int=3) -> float:
        """Measure distance in centimeters."""
        echo_time = np.mean([self.measure_us() for _ in range(nbr_measure)])
        return round( echo_time * self.cm_per_us + self.offset_cm )

    def _callback_rising(self, _gpio_id: int, _value: bool, tick: int):
        self.tic = tick

    def _callback_falling(self, _gpio_id: int, _value: bool, tick: int):
        self.toc = tick

    # @staticmethod
    # def calib():
    #     cm_per_us, offset_cm = np.polyfit(
    #         calib_cm_us[:, 1],
    #         calib_cm_us[:, 0], 
    #         deg=1
    #     )


# calib_cm_us = np.array([
#     [10, 658],
#     [20, 1210],
#     [30, 1773],
#     [40, 2358],
#     [50, 2894]
# ])



