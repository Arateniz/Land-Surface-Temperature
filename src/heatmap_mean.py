import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import os

if len(sys.argv[1:]) < 2:
	print("Not enough parameters specified!")
	quit()

print("\nStarting mean heatmap generation")
print("Opening submited dataset...")
filtered_day   = pd.read_csv(sys.argv[1], dtype=str).to_numpy()[:,6:]
filtered_night = pd.read_csv(sys.argv[2], dtype=str).to_numpy()[:,6:]

filtered_day   = np.where(filtered_day == "F", np.nan, filtered_day).astype(float)
filtered_night = np.where(filtered_night == "F", np.nan, filtered_night).astype(float)

masked_day     = np.ma.masked_array(filtered_day, np.isnan(filtered_day))
masked_night   = np.ma.masked_array(filtered_night, np.isnan(filtered_night))

arr_side = int(np.sqrt(masked_day.shape[1]))

mean_day       = np.ma.average(masked_day, axis = 0).reshape(arr_side, arr_side)
mean_night     = np.ma.average(masked_night, axis = 0).reshape(arr_side, arr_side)

min_temp=np.min(mean_night)
max_temp=np.max(mean_day)

os.system("tput cuu1")
os.system("tput el")
print("Opening submited dataset... Done!")


print("Generating heatmaps...")
fig  = plt.figure()

plt.title("Daytime")
plot = plt.imshow(mean_day, cmap = 'inferno', vmin=min_temp, vmax=max_temp)
plt.colorbar(plot)
fig.savefig("output/heatmap_day_mean.pdf")
plt.clf()

plt.title("Nighttime")
plot = plt.imshow(mean_night, cmap = 'inferno', vmin=min_temp, vmax=max_temp)
plt.colorbar(plot)
fig.savefig("output/heatmap_night_mean.pdf")
plt.close()

os.system("tput cuu1")
os.system("tput el")
print("Generating heatmaps... Done!")
