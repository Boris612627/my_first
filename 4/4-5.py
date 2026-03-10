import r2r_dac as r2r
import signal_generator as sg

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    dac = r2r.R2R_DAC(r2r.leds, 3.3)
    t = 0.0
    while True:
        v = amplitude*(sg.get_sin_wave_amplitude(signal_frequency, t))
        dac.set_voltage(v)
        sg.wait_for_sampling_period(sampling_frequency)
        t += 1/sampling_frequency
finally:
    dac.deinit()