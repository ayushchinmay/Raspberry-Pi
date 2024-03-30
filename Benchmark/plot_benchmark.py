"""
    AUTHOR      :   Ayush Chinmay
    DATE CREATED:   30 Mar 2024

    DESCRIPTION :  Code to start benchmark shell & plot the data from the CSV file

    ? CHANGELOG ?
        * [30 Mar 2024]
            - [x] Read the data from the CSV file
            - [x] Plot the data
            - [X] Save the plot
            - [X] Start benchmark.sh script from python

    ! TODO !
            - [X] Add functionality to plot the peaks for all the frames
"""

## ==========[ MODULES ]========== ##
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import subprocess
import os

## ==========[ CONSTANTS ]========== ##
# Directory to save the plots
PATH = f"{os.path.dirname(__file__)}/"
FNAME = None

os.chdir(PATH)

# If directory does not exist, create it
# Create Directory if it doesn't exist
if not os.path.exists(PATH):
    os.makedirs(PATH)

# Graph Styles
suptitle_font = {'family': 'sans', 'color': '#212529', 'weight': 'bold', 'style':'normal', 'size': 12}
label_font = {'family': 'sans', 'color': '#495057', 'weight': 'normal', 'style':'oblique', 'size': 10}
title_font = {'family': 'sans', 'color': '#212529', 'weight': 'bold', 'style':'normal', 'size': 10}
colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5"]

## ==========[ FUNCTIONS ]========== ##
# Read the data from the CSV file
def read_data():
    global FNAME

    data = pd.read_csv(PATH+'Results/'+'benchmark.csv')
    FNAME = data['Timestamp'][0].split()
    FNAME[1] = FNAME[1].replace(':', '-')
    data['CPU Throttled'] = data['CPU Throttled'].str.extract(r'throttled=(0x[0-9a-fA-F]+)')[0].apply(lambda x: int(x, 16))
    data['Timestamp'] = pd.to_datetime(data['Timestamp']) # .dt.strftime('%H:%M:%S')
    print(f"File Read Successfully!")
    print(data.head())
    return data


def plot_data(data, save=False):
    global FNAME 
    # Plot the data
    fig = plt.figure(facecolor='#f5f5f5', figsize=(8,5), dpi=200)
    fig.suptitle(f"Benchmark Results: {FNAME[0]} | {FNAME[1].replace('-',':')}", fontdict=title_font)

    # Create subplots
    axs = fig.subplots(3, 1, sharex=True)
    fig.align_ylabels(axs)

    # Set major ticks at every minute and minor ticks at 15-second intervals
    axs[-1].xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
    axs[-1].xaxis.set_minor_locator(mdates.SecondLocator(interval=15))
    axs[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    # Configure the axes
    for ax in axs:
        ax.set_xlim(data['Timestamp'].iloc[0], data['Timestamp'].iloc[-1])
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-.', linewidth='0.45', color='#ababab')
        ax.grid(which='minor', linestyle='--', linewidth='0.35', color='#cbcbcb')

    # Plot the data
    temp_max = max(data['CPU Temperature (°C)'])
    temp_min = min(data['CPU Temperature (°C)'])
    clock_max = max(data['CPU Clock Speed (MHz)'])
    clock_min = min(data['CPU Clock Speed (MHz)'])

    axs[0].set_ylabel("Temperature (°C)", fontdict=label_font)
    axs[0].set_ylim(temp_min-2, temp_max+2)
    axs[0].axhline(y=temp_max, color=colors[4], linestyle='--', linewidth=0.75, label='Max Temperature')
    axs[0].axhline(y=temp_min, color=colors[4], linestyle='--', linewidth=0.75, label='Max Temperature')
    axs[0].text(data['Timestamp'][100], temp_max+0.75, f"Max: {temp_max:.2f} °C", color=colors[4], size=6, bbox=dict(facecolor='white', edgecolor='#ffffff', pad=1.15))
    axs[0].text(data['Timestamp'][100], temp_min+0.75, f"Min: {temp_min:.2f} °C", color=colors[4], size=6, bbox=dict(facecolor='white', edgecolor='#ffffff', pad=1.15))
    axs[0].plot(data['Timestamp'], data['CPU Temperature (°C)'], linewidth=0.95, color=colors[0], label='CPU Temperature (°C)')
    
    axs[1].set_ylabel("Frequency (MHz)", fontdict=label_font)
    axs[1].set_ylim(clock_min-200, clock_max+200)
    axs[1].axhline(y=clock_max, color=colors[4], linestyle='--', linewidth=0.75, label='Max Clock Speed')
    axs[1].axhline(y=clock_min, color=colors[4], linestyle='--', linewidth=0.75, label='Min Clock Speed')
    axs[1].text(data['Timestamp'][100], clock_max+75, f"Max: {clock_max} MHz", color=colors[4], size=6, bbox=dict(facecolor='white', edgecolor='#ffffff', pad=1.15))
    axs[1].text(data['Timestamp'][100], clock_min+75, f"Min: {clock_min} MHz", color=colors[4], size=6, bbox=dict(facecolor='white', edgecolor='#ffffff', pad=1.15))
    axs[1].plot(data['Timestamp'], data['CPU Clock Speed (MHz)'], linewidth=0.95, color=colors[1], label='CPU Clock Speed (MHz)')

    axs[2].set_xlabel("Time (HH:MM:SS)", fontdict=label_font)
    axs[2].set_ylabel("Throttled (hex)", fontdict=label_font)
    axs[2].plot(data['Timestamp'], data['CPU Throttled'], linewidth=0.95, color=colors[2], label='Throttled')

    plt.tight_layout()

    # Save the plot
    if save:
        plt.savefig(PATH+'Results/'+f"benchmark_{FNAME[0]}_{FNAME[1]}.png")
        print(f"Plot saved as: {PATH}Results/benchmark_{FNAME[0]}_{FNAME[1]}.png")
    plt.show()


## ==========[ MAIN ]========== ##
def main():
    # Start the benchmark shell
    subprocess.run([f"{PATH}benchmark.sh"])
    # Read the data from the CSV file
    data = read_data()
    # Plot the data
    plot_data(data, True)


if __name__ == '__main__':
    main()
