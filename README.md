# Raspberry-Pi Projects
Projects based on Raspberry Pi platform.

## [PiCam](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiCam)
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/picam.png" width="800">

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
#### Usage
- Run the piCam.py python script. The dual live-preview windows should be visible.
- To capture an image, press the button once and release; the image captures from both cameras will be saved in the Stills directory.
- To close cameras and exit, press 'CTRL+C'
#### Notes
- Modify the `PATH` constant to match the project directory path
- Modify the `BUTTON_PIN` constant to match the GPIO pin connection with the button
- `PREV_WIDTH` and `PREV_HEIGHT` constants can be modified to adjust the live-preview window sizes.

## [Benchmark](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/Benchmark)
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/benchmark.png" width="800">

### Files
- **benchmark.sh**: Shell script to start *stress commandline tool* and save the data as a csv file
- **plot_benchmark.py**: Python script that starts the *benchmark.sh* script, and plot the data from the csv file
### Setup
- Install the stress commandline tool: `sudo apt install -y stress`
- Install required python packages: `matplotlib`, `pandas`
- Change current directory to the Benchmark folder: `cd Benchmark/`
- In the terminal type `chmod +x benchmark.sh` to make the file executable
- Start the python script with: `python plot_benchmark.py`. The benchmarking will take ~5 minutes, and the graph will be saved in *./Results/* directory.
