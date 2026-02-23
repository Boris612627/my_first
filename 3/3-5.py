import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)

led = 26

gpio.setup(led, gpio.OUT)

detekt = 6

gpio.setup(detekt, gpio.IN)

state = 0

while True:
    if gpio.input(detekt):
        state = 0
    else:
        state = 1
    gpio.output(led, state)