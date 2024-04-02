## Raspberry-Pi Projects
Projects based on Raspberry Pi platform.
#### [Pi Camera](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiCam)
- Implements face-detection and smile detection to trigger image-capture after 3 seconds of continuous smiling.
- Implements handling of dual mounted cameras simultaneously.
- Non-blocking button press detection to trigger image-capture events.
#### [Pi Mic](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiMic)
- Implements pyaudio to record audio through a usb microphone
- Push-to-Record button implemented, which upon release saves the audio as a WAV file
- Plots the recorded audio form for further audio analysis
#### [Pi Search](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiSearch)
- Non-blocking button press event checking
- Implemented image-capture-and-save trigger upon button press.
- Implemented audio stream capture as a push-to-record mode
- Added safe application termination
#### [Benchmark Tool](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/Benchmark)
- Utilizes a shell script to begin stress-test on all available cores
- Saves the stress test results (clock speeds, temperatures) as a CSV file.
- Plots the data over time and saves it as an image.
#### Overclocking Tutorial
- Overclocking, and stress testing to ensure stable operation.
#### GUI Remote Desktop for Raspberry Pi 5
- Set-up Raspberry Pi for operation without a connected monitor
- Find the local IP address, and contron the Raspberry Pi through a VNC Viewer

# [PiCam](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiCam)
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/picam.png" width="480">
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/picam_smile.png" width="480">

### Components:
- Raspberry Pi 5 (8GB) with Raspian OS (bookworm)
- IMX219 Camera Module V2
- Push-Button

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

# [PiMic](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiMic)
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/pimic.png" width="600">

### Components:
- Raspberry Pi 5 (8GB) with Raspian OS (bookworm)
- USB Microphone
- Push-Button

### Setup:
#### Update Config.txt
- Make the following modifications to the config.txt in boot/firmware/config.txt
```
.
dtparam=audio=0
audio_pwm_mode=2
.
```
- For additional audio software software information, refer to [PyAydui Documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/)
#### Installing PyAudio module in python
- In the terminal, run the following commands: `sudo apt update` and `sudo apt full-upgrade`
- Ensure the USB Mic shows up with the following command: `lsusb -t`
- Test the mic is detected by using the following command: `arecord -l`
- Install the PiCamera2 python module: `sudo apt install -y python3-pyaudio`
### Usage
- As of now, the *piMic.py* script will use the default audio device to record sound.
- To start recording audio, press the button and hold; The audio will be recorded until the button is released.
- The Audio files can be found in *./Recordings/* and the Waveform plots in *./Waveforms/*
- To terminate the mic and exit, press 'CTRL+C'
### Notes
- Modify the `PATH` constant to match the project directory path
- Modify the `BUTTON_PIN` constant to match the GPIO pin connection with the button
- Currently the script only implements MONO-channel recording

# [PiSearch](https://github.com/ayushchinmay/Raspberry-Pi/tree/main/PiSearch)
### Components:
- Raspberry Pi 5 (8GB) with Raspian OS (bookworm)
- IMX219 Camera Module V2
- USB Microphone
- Push-Button

<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/000677.png" width="600">
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/000678.png" width="600">

### Description
- This combines the functionality of PiCam & PiMic into one large script sans the plotting functions.
- When the button is pressed, the cameras will capture a still and save it to the *./Stills* directory.
- Right after this, the audio recording will begin
- The audio stream will be recorded for as long as the button is held
 	- Once the button is released, the audio stream will be saved as a wave file in *./Recordings*
	-  When the captures are saved, we will go back into the while loop, awaiting the next button press
-  To exit the script safely, press `CTRL+C`. This will terminate the audio stream, and the camera previews, then exit.
### Notes
- This project is still in development, and more features will be added as it progresses.
- Some of those features may include audio transcription, object detection, web searches, setting timers, etc.

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

## Overclocking [Specific to Raspberry Pi 5]
<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/heatsink.jpg" height="275"> <img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/neofetch.png" height="275">

### Some Notes
- Before starting with overclocking, ensure sufficient heat dissipation solutions such as a heatsink or an [active cooling fan](https://wiki.geekworm.com/P511).
- Ensure the power supply is capable of handling higher currents. Using the Raspberry-Pi certified [power supply](https://www.raspberrypi.com/products/27w-power-supply/) is recommended.

### Setup
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
- For more information, refer to [Jeff Geerling: Overclocking & Underclocking Raspberry Pi 5](https://www.jeffgeerling.com/blog/2023/overclocking-and-underclocking-raspberry-pi-5)

## GUI Remote Desktop for Raspberry Pi
- While the Raspberry Pi 5 supports dual 4K at 60 fps, the micro-HDMI cables not being as abundant can lead to dull wait-times.
- We can alleviate this issue by enabling VNC on the board and control it remotely.
### Connect to Wifi
- If you did not provide the wifi credentials during the [Pi-Imager](https://www.raspberrypi.com/software/) setup, you may need to add the wifi credentials manually by creating a `wpa_supplicant.conf` file in the `/boot/` directory using a separate computer and a micro-SD card Reader.
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
	ssid="WIFI-NETWORK-IDENTIFIER"
	psk="WIFI-SECURITY-KEY"
}
```
- For now you can try connecting to the raspberry pi in headless-mode (through SSH). Open a terminal in a separate computer connected to the same network, and type `ssh <user_name>@<device_name>.local`. Replace the `<user_name>` and `<device_name>` with the values used during setup.
- You can retrieve the local IP address by typing `hostname -I` in the terminal. This IP address will be used when connecting through VNC Viewer.
- Enable VNC on device by typing `sudo raspi-config` in the SSH terminal. Navigate to **Interface Options -> VNC -> Enable**

<img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/config1.png" height="275"> <img src="https://github.com/ayushchinmay/Raspberry-Pi/blob/main/readme_img/config2.png" height="275">

- Download a [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/) and connect to the Raspberry Pi using setup credentials.
- Follow this informative tutorial from [Real VNC](https://help.realvnc.com/hc/en-us/articles/360003474552-How-do-I-get-started-with-RealVNC-Connect-on-Windows#on-the-device-you-want-to-control-0-0). 
