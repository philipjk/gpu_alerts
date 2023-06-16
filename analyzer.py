import matplotlib.pyplot as plt
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
plt.rcParams["font.family"] = "serif"

points = 6

# Read the csv file
df = pd.read_csv("06-15-20-05.csv")
for i in range(8):
    # Select the data for the i-th gpu
    gpu = df[df['gpu_index'] == i]
    # Convert the time to datetime format
    gpu['time'] = pd.to_datetime(gpu['time'], format='%m-%dT%H:%M')
    # Set the time as index
    gpu.set_index('time', inplace=True)
    # smooth the temperature data
    gpu['temperature'] = gpu['temperature'].rolling(points).mean()
    # Plot the temperature
    gpu['temperature'].plot()
plt.legend(range(8))
plt.ylabel("Temperature (°C)")
plt.grid()
plt.title(f"GPU temperature (rolling average over {points*5} minutes)")
plt.savefig("temperature.png")

# do the same for utilization in a new figure
plt.figure()
for i in range(8):
    gpu = df[df['gpu_index'] == i]
    gpu['time'] = pd.to_datetime(gpu['time'], format='%m-%dT%H:%M')
    gpu.set_index('time', inplace=True)
    gpu['utilization'] = gpu['utilization'].rolling(points).mean()
    gpu['utilization'].plot()
plt.legend(range(8))
plt.ylabel("Utilization (%)")
plt.grid()
plt.title(f"GPU utilization (rolling average over {points*5} minutes)")
plt.savefig("utilization.png")