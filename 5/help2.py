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
        """Очистка GPIO"""
        gpio.output(self.bits_gpio, 0)
        gpio.cleanup()

    def number_to_dac(self, number):
        """Подача числа на ЦАП"""
        for i, pin in enumerate(self.bits_gpio):
            bit_value = (number >> (7 - i)) & 1
            gpio.output(pin, bit_value)  # можно просто bit_value (0 или 1)
    
    def sequential_counting_adc(self):
        """
        Метод последовательного счёта
        Возвращает цифровой код (0-255)
        """
        for code in range(256):
            # Подаём код на ЦАП
            self.number_to_dac(code)
            
            # Ждём реакции компаратора
            time.sleep(self.compare_time)
            
            # Читаем компаратор
            if gpio.input(self.comp_gpio) == gpio.HIGH:
                if self.verbose:
                    print(f"Найдено превышение при code={code}")
                return code
        
        # Если дошли до максимума - входное напряжение выше диапазона
        if self.verbose:
            print(f"Внимание: входное напряжение превышает {self.dynamic_range}В")
        return 255
    
    def get_sc_voltage(self):
        """Измерение напряжения в вольтах"""
        code = self.sequential_counting_adc()
        voltage = (code / 255.0) * self.dynamic_range
        return voltage

# Основной охранник
if __name__ == "__main__":
    # Измерьте реальный динамический диапазон мультиметром!
    DYNAMIC_RANGE = 3.3  # Замените на измеренное значение
    
    adc = None
    
    try:
        adc = R2R_ADC(DYNAMIC_RANGE, compare_time=0.01, verbose=False)
        print("Начинаю измерения... Нажмите Ctrl+C для остановки")
        
        while True:
            voltage = adc.get_sc_voltage()
            print(f"U = {voltage:.3f} В")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nИзмерения остановлены")
    finally:
        if adc:
            adc.deinit()
        else:
            gpio.cleanup()
        print("Программа завершена")
