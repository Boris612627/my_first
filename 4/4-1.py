import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]
gpio.setup(dac_bits, gpio.OUT)

dynamic_range = 3.133

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапозон ЦАП (0.00 - {dynamic_range:.2f} B)")
        print("Устонавливаем 0.0 B")
        return 0
    return int(voltage/dynamic_range * 255)

def number_to_dac(number):
    number = number%255
    return [int(element) for element in bin(number)[2:].zfill(8)]

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
            gpio.output(dac_bits, number_to_dac(number))
        except ValueError:
            print("Вы ввели не число. Попробуй еще раз\n") 
finally:
    gpio.output(dac_bits, 0)
    gpio.cleanup()