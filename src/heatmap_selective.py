import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import os

if len(sys.argv[1:]) < 4:
	print("Not enough parameters specified!")
	quit()

print("\nStarting heatmap generation")
print("Opening submited dataset...")
year                = int(sys.argv[1])
next_year           = year + 1
stats_day           = pd.read_csv(sys.argv[2], dtype=str)
filtered_day_data   = pd.read_csv(sys.argv[3], dtype=str)
filtered_night_data = pd.read_csv(sys.argv[4], dtype=str)

dates_range    = (stats_day["date"] >= str(year)+"-01-01") & (stats_day["date"] < str(next_year)+"-01-01")
stats_day      = stats_day.loc[dates_range]
temp_df        = filtered_day_data.iloc[:,2]
dates_range    = (temp_df >= "A"+str(year)+"001") & (temp_df < "A"+str(next_year)+"001")
filtered_day   = filtered_day_data.loc[dates_range].to_numpy()[:,6:]
filtered_night = filtered_night_data.loc[dates_range].to_numpy()[:,6:]

filtered_day   = np.where(filtered_day == "F", np.nan, filtered_day).astype(float)
filtered_night = np.where(filtered_night == "F", np.nan, filtered_night).astype(float)

arr_side = int(np.sqrt(filtered_day.shape[1]))
dates    = filtered_day.shape[0]
os.system("tput cuu1")
os.system("tput el")
print("Opening submited dataset... Done!")

print("Generating heatmaps...")
print()
for i in range(dates):
	os.system("tput cuu1")
	os.system("tput el")
	print("\tProgress ", i, "/", dates)

	heatmap_day   = np.resize(filtered_day[i,:], (arr_side, arr_side))
	heatmap_night = np.resize(filtered_night[i,:], (arr_side, arr_side))

	fig  = plt.figure()
	date = stats_day["date"].iloc[i]

	plot = plt.imshow(heatmap_day, cmap = 'inferno')
	plt.colorbar(plot)
	plt.title(str(date) + " — Daytime")
	fig.savefig("output/heatmaps/heatmap_day_" + str(date) + ".pdf")
	plt.clf()

	plt.title(str(date) + " — Nighttime")
	plot = plt.imshow(heatmap_night, cmap = 'inferno')
	plt.colorbar(plot)
	fig.savefig("output/heatmaps/heatmap_night_" + str(date) + ".pdf")

	plt.close()

os.system("tput cuu1")
os.system("tput el")
os.system("tput cuu1")
os.system("tput el")
print("Generating heatmaps... Done!")

print("Generating mean heatmap of " + str(year) + "...")
masked_day     = np.ma.masked_array(filtered_day, np.isnan(filtered_day))
masked_night   = np.ma.masked_array(filtered_night, np.isnan(filtered_night))

arr_side = int(np.sqrt(masked_day.shape[1]))

mean_day       = np.ma.average(masked_day, axis = 0).reshape(arr_side, arr_side)
mean_night     = np.ma.average(masked_night, axis = 0).reshape(arr_side, arr_side)

min_temp=np.min(mean_night)
max_temp=np.max(mean_day)

fig  = plt.figure()

plot = plt.imshow(mean_day, cmap = 'inferno', vmin=min_temp, vmax=max_temp)
plt.colorbar(plot)
plt.title("Mean heatmap of " + str(year) + " — Daytime")
fig.savefig("output/heatmap_day_" + str(year) + ".pdf")
plt.clf()

plt.title("Mean heatmap of " + str(year) + " — Nighttime")
plot = plt.imshow(mean_night, cmap = 'inferno', vmin=min_temp, vmax=max_temp)
plt.colorbar(plot)
fig.savefig("output/heatmap_night_" + str(year) + ".pdf")

plt.close()
os.system("tput cuu1")
os.system("tput el")
print("Generating mean heatmap of " + str(year) + "... Done!")
