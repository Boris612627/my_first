#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        """
        Конструктор класса АЦП последовательного счёта
        
        Параметры:
        dynamic_range - динамический диапазон АЦП (опорное напряжение в Вольтах)
        compare_time - время для сравнения компаратором
        verbose - режим отладки (печать промежуточных значений)
        """
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        self.verbose = verbose
        
        # Пины для 8-битного ЦАП (от старшего к младшему)
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        # Пин, подключённый к выходу компаратора
        self.comp_gpio = 21
        
        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.comp_gpio, GPIO.IN)
        
        if self.verbose:
            print(f"АЦП инициализирован: диапазон {dynamic_range}В, время сравнения {compare_time}с")
    
    def __del__(self):
        """Деструктор класса - очистка GPIO"""
        self.cleanup()
    
    def cleanup(self):
        """Очистка настроек GPIO и установка 0 на выходе ЦАП"""
        # Устанавливаем 0 на всех пинах ЦАП
        for pin in self.bits_gpio:
            GPIO.output(pin, GPIO.LOW)
        
        # Очищаем настройки GPIO
        GPIO.cleanup()
        
        if self.verbose:
            print("GPIO очищен")
    
    def number_to_dac(self, number):
        """
        Подаёт число number (0-255) на параллельный вход ЦАП
        
        Параметры:
        number - целое число от 0 до 255
        """
        if number < 0 or number > 255:
            raise ValueError("Число должно быть в диапазоне 0-255")
        
        # Подаём число на пины ЦАП (от старшего бита к младшему)
        for i, pin in enumerate(self.bits_gpio):
            # Проверяем i-й бит числа (считая от старшего)
            bit_value = (number >> (7 - i)) & 1
            GPIO.output(pin, GPIO.HIGH if bit_value else GPIO.LOW)
        
        if self.verbose:
            print(f"Установлено число {number} на ЦАП (0x{number:02X})")
    
    def sequential_counting_adc(self):
        """
        Метод последовательного счёта для измерения входного напряжения
        
        Возвращает:
        digit - цифровой код измеренного напряжения (0-255)
        """
        # Перебираем все возможные значения от 0 до 255
        for code in range(256):
            # Подаём текущий код на ЦАП
            self.number_to_dac(code)
            
            # Ждём, пока компаратор сравнит напряжения
            time.sleep(self.compare_time)
            
            # Читаем состояние компаратора
            # Если компаратор выдал 1 (HIGH) - напряжение ЦАП превысило входное
            if GPIO.input(self.comp_gpio) == GPIO.HIGH:
                if self.verbose:
                    print(f"Найдено превышение при коде {code}")
                return code
            
            if self.verbose:
                print(f"Код {code}: компаратор = {GPIO.input(self.comp_gpio)}")
        
        # Если превышение не найдено - возвращаем максимум
        if self.verbose:
            print("Превышение не найдено, возвращаю максимум 255")
        return 255
    
    def get_sc_voltage(self):
        """
        Измеряет напряжение методом последовательного счёта
        
        Возвращает:
        voltage - измеренное напряжение в Вольтах
        """
        # Получаем цифровой код
        code = self.sequential_counting_adc()
        
        # Переводим в напряжение
        # U = (code / 255) * dynamic_range
        voltage = (code / 255.0) * self.dynamic_range
        
        if self.verbose:
            print(f"Измерено: код={code}, напряжение={voltage:.3f}В")
        
        return voltage

# Основной охранник
if __name__ == "__main__":
    # ЗНАЧЕНИЕ ДИНАМИЧЕСКОГО ДИАПАЗОНА НУЖНО ИЗМЕРИТЬ МУЛЬТИМЕТРОМ!
    # Обычно это около 3.3В, но может отличаться
    
    DYNAMIC_RANGE = 3.3  # Временное значение, замените на измеренное!
    
    adc = None
    
    try:
        # Создаём объект АЦП
        # Для отладки можно включить verbose=True
        adc = R2R_ADC(DYNAMIC_RANGE, compare_time=0.01, verbose=False)
        
        print("Начинаю измерения напряжения...")
        print("Нажмите Ctrl+C для остановки")
        print("-" * 40)
        
        # Бесконечный цикл измерений
        while True:
            # Измеряем напряжение
            voltage = adc.get_sc_voltage()
            
            # Выводим результат с 3 знаками после запятой
            print(f"U = {voltage:.3f} В")
            
            # Небольшая задержка между измерениями
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nИзмерения остановлены пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Гарантированно очищаем GPIO
        if adc:
            adc.cleanup()
        else:
            GPIO.cleanup()
        print("Программа завершена")
