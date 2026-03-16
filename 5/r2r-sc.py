import r2r_adc as r2r
import time
import matplotlib.pyplot as plt

adc = r2r.R2R_ADC(3.1, 0.0001)
voltage_values = []
time_values = []
duration = 3.0

try:
    st = time.time()
    while (time.time() - st) < duration:
        