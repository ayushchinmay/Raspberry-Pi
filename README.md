## Raspberry-Pi Projects
Projects based on Raspberry Pi platform.
#### [Pi Camera](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiCam)
- Implements face-detection and smile detection to trigger image-capture after 3 seconds of continuous smiling.
- Implements handling of dual mounted cameras simultaneously.
- Non-blocking button press detection to trigger image-capture events.
#### [Benchmark Tool](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/Benchmark)
- Utilizes a shell script to begin stress-test on all available cores
- Saves the stress test results (clock speeds, temperatures) as a CSV file.
- Plots the data over time and saves it as an image.

# [PiCam](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiCam)
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/picam.png" width="480">
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/picam_smile.png" width="480">

### Components:
- Raspberry Pi 5 (8GB) with Raspian OS (bookworm)
- IMX219 Camera Module V2
- Push-Button
- Instantiates the dual-camera preview
### Setup:
#### Update Config.txt
- Make the following modifications to the config.txt in boot/firmware/config.txt
```
.
camera_auto_detect=0     # Disables auto-detection for third-party camera modules
dtoverlay=imx219,cam0    # Setup cam0 with the specified sensor
dtoverlay=imx219,cam1    # Make sure to replace 'imx219' with your camera sensor
.
```
- For additional camera software information, refer to [Raspberry Pi Documenation](https://www.raspberrypi.com/documentation/computers/camera_software.html)
#### Installing PiCamera2 module in python
- In the terminal, run the following commands: `sudo apt update` and `sudo apt full-upgrade`
- Test the cameras are detected by using the following command: `rpicam-hello --camera 0`
- Install the PiCamera2 python module: `sudo apt install -y python3-picamera2`
### Usage
- Run the piCam.py python script. The dual live-preview windows should be visible.
- To capture an image, press the button once and release; the image captures from both cameras will be saved in the Stills directory.
- To close cameras and exit, press 'CTRL+C'
### Notes
- Modify the `PATH` constant to match the project directory path
- Modify the `BUTTON_PIN` constant to match the GPIO pin connection with the button
- `PREV_WIDTH` and `PREV_HEIGHT` constants can be modified to adjust the live-preview window sizes.

# [Benchmark](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/Benchmark)
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/benchmark1.png" width="600">

### Files
- **benchmark.sh**: Shell script to start *stress commandline tool* and save the data as a csv file
- **plot_benchmark.py**: Python script that starts the *benchmark.sh* script, and plot the data from the csv file
### Setup
- Install the stress commandline tool: `sudo apt install -y stress`
- Install required python packages: `matplotlib`, `pandas`
- Change current directory to the Benchmark folder: `cd Benchmark/`
- In the terminal type `chmod +x benchmark.sh` to make the file executable
- Start the python script with: `python plot_benchmark.py`. The benchmarking will take ~5 minutes, and the graph will be saved in *./Results/* directory.
### Overclocking [Specific to Raspberry Pi 5]
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/heatsink.jpg" height="275"> <img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/neofetch.png" height="275">

#### Some Notes
- Before starting with overclocking, ensure sufficient heat dissipation solutions such as a heatsink or an [active cooling fan](https://wiki.geekworm.com/P511).
- Ensure the power supply is capable of handling higher currents. Using the Raspberry-Pi certified [power supply](https://www.raspberrypi.com/products/27w-power-supply/) is recommended.

#### Setup
- To overclock the Raspberry Pi, edit the config.txt using: `sudo nano /boot/firmware/config.txt`
```
.
arm_boost=1
overvoltage_delta=50000  # Voltage Delta: 50000uV = 0.05V
arm_freq=2800            # CPU Freq in MHz
gpu_freq=925             # GPU Freq in MHz
.
```
- Start with 2.6GHz Overclock and move up in increments of 500MHZ (testing for stability under stress)
- Reboot the Raspberry Pi using the following command in the terminal: `reboot`
- Run the stress test and ensure the Raspberry Pi is stable at the selected clock
- You can force the clock speed to remain at the OC by adding `force_turbo=1` in the *config.txt*
- Additionally, [Geekbench 6](https://www.geekbench.com/preview/) can be used for checking stability under realistic loads.
