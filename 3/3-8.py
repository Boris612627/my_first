import RPi.GPIO as gpio
import time 

def dec2bin(value):
    value = value%128
    return [int(element) for element in bin(value)[2:].zfill(7)]

gpio.setmode(gpio.BCM)

leds = [16, 12, 25, 17, 27, 22, 24]

gpio.setup(leds, gpio.OUT)

gpio.output(leds, 0)

buttom_up = 9

gpio.setup(buttom_up, gpio.IN)

buttom_down = 10

gpio.setup(buttom_down, gpio.IN)

num = 0

sleep_time = 0.2

while True:
    if gpio.input(buttom_up) and gpio.input(buttom_down):
        gpio.output(leds, [1, 1, 1, 1, 1, 1, 1])
        time.sleep(10)
        gpio.output(leds, dec2bin(num))
    if gpio.input(buttom_up):
        num += 1
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    if gpio.input(buttom_down):
        num -= 1
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    gpio.output(leds, dec2bin(num))