import RPi.GPIO as gpio
import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые значения")
        
        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
        
        first_byte = (number >> 4) & 0xFF  # Старшие 8 бит (включая конфигурационные биты)
        second_byte = ((number & 0xF) << 4) | 0x00  # Младшие 4 бита + заполнение нулями
        
        self.bus.write_i2c_block_data(self.address, 0x40, [first_byte, second_byte])  # Команда быстрой записи
        
        if self.verbose:
            print(f"Число: {number}, отправленые по I2C данные: [0x{(self.address<<1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} V)")
            voltage = 0.0
        self.set_number(int(voltage / self.dynamic_range * 4095))  # Правильно масштабируем до 12 бит

if __name__ == "__main__":
    try:
        dac = MCP4725(5, 0x61, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз.")

    finally:
        dac.deinit()
