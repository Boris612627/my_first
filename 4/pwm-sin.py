import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3
something = 500
signal_frequency = 10
sampling_frequency = 1000

try:
    pwm = pwm.PWM_DAC(12, something, amplitude, True)
    t = 0.0
    while True:
        v = amplitude * (sg.get_sin_wave_amplitude(signal_frequency, t))
        pwm.set_voltage(v)
        sg.wait_for_sampling_period(sampling_frequency)
        t += 1 / sampling_frequency

finally:
    pwm.deinit()