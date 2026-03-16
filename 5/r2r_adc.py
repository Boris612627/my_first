import RPi.GPIO as gpio
import time
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        gpio.setmode(gpio.BCM)
        gpio.setup(self.bits_gpio, gpio.OUT, initial=0)
        gpio.setup(self.comp_gpio, gpio.IN)

    def deinit(self):
        gpio.output(self.bits_gpio, 0)
        gpio.cleanup()