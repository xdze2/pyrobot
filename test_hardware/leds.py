



from pyrobot.gpio_mapping import OnboardLEDGpio
import pigpio
import time


gpio = pigpio.pi()



for pin in OnboardLEDGpio:
    gpio.set_mode(pin, pigpio.OUTPUT)
    gpio.write(pin, 1)
    print(gpio.read(pin))
    time.sleep(0.5)
    gpio.write(pin, 0)