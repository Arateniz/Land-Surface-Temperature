import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import os

if len(sys.argv[1:]) < 3:
	print("Not enough parameters specified!")
	quit()

print("\nStarting graph generation")
print("Opening submited dataset...")
year           = int(sys.argv[1])
next_year      = year + 1
stats_day      = pd.read_csv(sys.argv[2], dtype={"date[YYYYDDD]":              str,
													"date":                    str,
													"product":                 str,
													"band":                    str,
													"min":                     float,
													"max":                     float,
													"sum":                     float,
													"range":                   float,
													"mean":                    float,
													"variance":                float,
													"standard_deviation":      float,
													"tot_pixels":              int,
													"pixels_pass_qa":          int,
													"per_cent_pixels_pass_qa": float})

stats_night    = pd.read_csv(sys.argv[3], dtype={"date[YYYYDDD]":              str,
													"date":                    str,
													"product":                 str,
													"band":                    str,
													"min":                     float,
													"max":                     float,
													"sum":                     float,
													"range":                   float,
													"mean":                    float,
													"variance":                float,
													"standard_deviation":      float,
													"tot_pixels":              int,
													"pixels_pass_qa":          int,
													"per_cent_pixels_pass_qa": float})

dates_range    = (stats_day["date"] >= str(year)+"-01-01") & (stats_day["date"] < str(next_year)+"-01-01")
stats_day      = stats_day.loc[dates_range]
stats_night    = stats_night.loc[dates_range]

os.system("tput cuu1")
os.system("tput el")
print("Opening submited dataset... Done!")

print("Generating graphs...")
fig = plt.figure()
plt.title(str(year))
plt.tick_params(axis = "x", bottom = False, labelbottom = False)
plt.tick_params(axis = "y", left = False, labelleft = False)
ax = fig.add_subplot(111)
plt.xticks(rotation=60)
ax.tick_params(axis = "x", labelsize = 8)

ax.plot(stats_night["date"].str.replace(str(year)+"-", ""), stats_night["mean"], label = "Night")
ax.errorbar(stats_night["date"].str.replace(str(year)+"-", ""),
				stats_night["mean"],
				yerr = stats_night["standard_deviation"],
				capsize = 2,
				color = "black",
				fmt   = " ")

ax.plot(stats_day["date"].str.replace(str(year)+"-", ""), stats_day["mean"], label = "Day")
ax.errorbar(stats_day["date"].str.replace(str(year)+"-", ""),
				stats_day["mean"],
				yerr = stats_day["standard_deviation"],
				capsize = 2,
				color = "black",
				fmt   = " ")


ax.legend(loc = "upper right")
fig.savefig("output/graph_" + str(year) + ".pdf")
plt.close()

os.system("tput cuu1")
os.system("tput el")
print("Generating graphs... Done!")
