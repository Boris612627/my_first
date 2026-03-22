import matplotlib.pyplot as plt
def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.title('График')
    plt.xlabel('Напряжение, В')
    plt.ylabel('Время, с')
    plt.show()
    