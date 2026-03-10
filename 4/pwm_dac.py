import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        gpio.setup(self.gpio_pin, gpio.OUT, initial=0)

        self.pwm = gpio.PWM(self.gpio_pin, self.pwm_frequency)


    def deinit(self):
        self.pwm.stop()
        gpio.output(self.gpio_pin, 0)
        gpio.cleanup()

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапозон ЦАП (0.00 - {self.dynamic_range:.2f} B)")
            print("Устонавливаем 0.0 B")
            voltage = 0.0
        duty_cycle = (voltage / self.dynamic_range)*100
        self.pwm.ChangeDutyCycle(duty_cycle)
        print(f"Коэффициент заполнения: {duty_cycle}")


if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.133, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")

    finally:
        dac.deinit()