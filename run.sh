#!/bin/zsh

echo "Available datasets:"
ls -l src/data | grep "dr" | awk '{print NR". " $9}' | tr "_" " "
echo -n "Choose file: "
read choice
echo -n "Specify year: "
read year
input_dir=$(ls -l src/data | grep "dr" | awk 'NR=='$choice'{printf $9}')

echo
echo "Preparing output directory..."
if [ -d "output" ]
then
	rm -rf output
fi
mkdir -p output/heatmaps
tput cuu1
tput el
echo "Preparing output directory... Done!"

python3 src/heatmap_selective.py $year src/data/$input_dir/statistics_day.csv src/data/$input_dir/filtered_day.csv src/data/$input_dir/filtered_night.csv

python3 src/heatmap_mean.py src/data/$input_dir/filtered_day.csv src/data/$input_dir/filtered_night.csv

python3 src/graph_selective.py $year src/data/$input_dir/statistics_day.csv src/data/$input_dir/statistics_night.csv
