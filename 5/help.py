#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from r2r_adc import R2R_ADC  # импортируем ваш класс из предыдущего задания
from adc_plot import plot_voltage_vs_time

def main():
    # Настройки эксперимента
    DYNAMIC_RANGE = 3.3      # Измерьте реальное значение мультиметром!
    COMPARE_TIME = 0.0001    # 100 мкс - малое время для быстрых измерений
    DURATION = 3.0            # Продолжительность измерений в секундах
    
    # Списки для хранения данных
    voltage_values = []
    time_values = []
    
    # Создаём объект АЦП
    adc = None
    
    try:
        print(f"Запуск измерений на {DURATION} секунд...")
        print(f"Динамический диапазон: {DYNAMIC_RANGE} В")
        print(f"Время сравнения: {COMPARE_TIME} с")
        print("-" * 50)
        
        # Создаём объект АЦП с малым временем сравнения
        adc = R2R_ADC(DYNAMIC_RANGE, compare_time=COMPARE_TIME, verbose=False)
        
        # Запоминаем время старта
        start_time = time.time()
        last_print = start_time
        
        # Измеряем, пока не пройдёт DURATION секунд
        while time.time() - start_time < DURATION:
            # Текущее время от начала эксперимента
            current_time = time.time() - start_time
            
            # Измеряем напряжение
            voltage = adc.get_sc_voltage()
            
            # Сохраняем данные
            time_values.append(current_time)
            voltage_values.append(voltage)
            
            # Печатаем прогресс каждые 0.5 секунды
            if current_time - last_print >= 0.5:
                print(f"Время: {current_time:.2f} с, U = {voltage:.3f} В")
                last_print = current_time
        
        print(f"\nИзмерения завершены. Получено {len(voltage_values)} точек")
        print(f"Средняя частота: {len(voltage_values)/DURATION:.1f} Гц")
        print("-" * 50)
        print("Строю график...")
        
        # Строим график
        plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
        
    except KeyboardInterrupt:
        print("\nИзмерения прерваны пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Очищаем GPIO
        if adc:
            adc.deinit()
            print("GPIO очищен")

if __name__ == "__main__":
    main()
