import time
from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time

def main():
    DYNAMIC_RANGE = 5.0      
    DURATION = 3.0
    
    voltage_values = []
    time_values = []
    
    adc = None
    
    try:
        adc = MCP3021(DYNAMIC_RANGE, verbose=False)
        
        start_time = time.time()
        last_print = start_time
        
        while time.time() - start_time < DURATION:
            current_time = time.time() - start_time
            
            voltage = adc.get_voltage()
            
            time_values.append(current_time)
            voltage_values.append(voltage)
            
            if current_time - last_print >= 0.5:
                print(f"Время: {current_time:.2f} с, U = {voltage:.3f} В")
                last_print = current_time
        
        plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
        
    finally:
        if adc:
            adc.deinit()

if __name__ == "__main__":
    main()