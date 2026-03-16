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

    def number_to_dac(self, number):
        for i, pin in enumerate(self.bits_gpio):
            bit_value = (number >> (7 - i)) & 1
            gpio.output(pin, gpio.HIGH if bit_value else gpio.LOW)
    def sequential_counting_adc(self):
        for code in range(256):
            self.number_to_dac(code)
            
            time.sleep(self.compare_time)
        return 255
    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        voltage = (code / 255.0) * self.dynamic_range
        return voltage

    
# Основной охранник
if __name__ == "__main__":
    
    DYNAMIC_RANGE = 2
    
    adc = None
    
    try:
        adc = R2R_ADC(DYNAMIC_RANGE, compare_time=0.01, verbose=False)
        
        while True:
            voltage = adc.get_sc_voltage()
            print(f"U = {voltage:.3f} В")
            
            time.sleep(0.5)
    finally:
        adc.deinit()
        if adc:
            adc.cleanup()
        else:
            gpio.cleanup()