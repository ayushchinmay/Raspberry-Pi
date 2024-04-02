"""
	AUTHOR      :   Ayush Chinmay, Vigneshwer Ramamoorthi
	DATE CREATED:   21 Mar 2024

	DESCRIPTION :   Python code to capture images and audio using Raspberry Pi Camera Module and Microphone

	COMPONENTS:
			- Raspberry Pi 5 ()
			- Raspberry Pi Camera Module
			- Microphone
			- Speaker
			- Battery Pack

	? CHANGELOG ?
		* [21 Mar 2024]
			- [ ] ...

	! TODO !
			- [-] Initialization functions for Camera and Microphone
			- [-] Detect button press
			- [-] Detect button release
			- [-] Capture Image on button press
			- [-] Record Audio on button press
			- [-] Stop Recording on button release
			- [-] Save Image and Audio to a file
			- [ ] Send Image and Audio to an API for processing
			- [ ] Receive API response and display it on the screen
"""

## ==========[ MODULES ]========== ##
import os
from gpiozero import Button
from time import sleep, strftime
from picamera2 import Picamera2, Preview
from pyaudio import PyAudio, paInt16
import wave
import numpy as np

## Constants
PATH = "/home/ayush-pi/Documents/PyCode/PiSearch/"  # Directory Path
STILLS = PATH + "Stills/"
RECORDINGS = PATH + "Recordings/"

# Create Directory if it doesn't exist
try:
	os.makedirs(STILLS)
	os.makedirs(RECORDINGS)
except:
	pass

## ==========[ CONFIGURATION ]========== ##
## Buttons
BUTTON_PIN = 26
button = None

# Colors for plotting
colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5"]

## ==========[ CAMERA CONFIGURATION ]========== ##
# Camera
PREV_WIDTH = 820			# Preview Width
PREV_HEIGHT = 616			# Preview Height

## Configuration
main_config={'size': (3280, 2464), 'format': 'XBGR8888'}
lores = {'size': (1640, 1232), 'format': 'XBGR8888'}
preview_config = None
capture_config = None

## Controls
control0 = {'AwbEnable': False, 'ColourGains': (0.9, 0.8), 'AeEnable': True, 'NoiseReductionMode': 2}
control1 = {'AwbEnable': True, 'AeEnable': True, 'NoiseReductionMode': 2}

## Cameras
cam0 = None
cam1 = None

## ==========[ MICROPHONE CONFIGURATION ]========== ##
# Microphone
mic = None
DEVICE = None
SAMPLE_RATE = None
CHANNELS = 1    # int(mic.get_device_info_by_index(DEVICE)['maxInputChannels'])
CHUNK = 4096
FORMAT = paInt16

# Frames
frames = None
stream = None
info = True

## ==========[ HELPERS ]========== ##
# Do Nothing
def do_nothing():
	sleep(3)

# Print Camera Info
def print_cam_info(data):
	print("    {")
	for key in data:
		print(f"\t{key}: {data[key]}")
	print("    }")
	
# Show available devices
def show_audio_devices():
	p = PyAudio()
	for i in range(p.get_device_count()):
		dev = p.get_device_info_by_index(i)
		print((i,dev['name'],dev['maxInputChannels']))
	print(p.get_default_input_device_info())
# (0, 'USB PnP Sound Device: Audio (hw:0,0)', 1)
	
## ==========[ CAMERA FUNCTIONS ]========== ##
# Start Camera function
def start_camera(camnum, controls, preview=True):
	global preview_config, capture_config

	print(f"[INFO] Starting Camera {camnum}")
	# Initialize Camera
	cam = Picamera2(camera_num=camnum)
	# Create Config
	preview_config = cam.create_preview_configuration(main=main_config, lores=lores, display="lores")
	cam.configure(preview_config)
	capture_config = cam.create_still_configuration()
	# Set Controls
	cam.set_controls(controls)
	# Start Preview
	if preview: # If Preview is True, show the preview, else start preview with NULL
		cam.start_preview(Preview.QTGL, x=10, width=PREV_WIDTH, height=PREV_HEIGHT)
	else:
		cam.start_preview(Preview.NULL)
	cam.start()
	print(f"\n[CAM {camnum}]")
	print("    Config: ")
	print_cam_info(preview_config)
	print("    Controls: ")
	print_cam_info(controls)
	return cam


# Stop Camera function
def stop_camera(cam):
	cam.close()
	print("[INFO] Camera Stopped")
	

# Take Picture function
def take_picture():
	print("[INFO] Taking Picture...")
	sleep(0.2)
	fname = f"image_{strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
	print("[INFO] Switching to Capture Mode: ")
	if cam0 is not None:
		cam0.switch_mode_and_capture_file(capture_config, STILLS+"cam0_"+fname)
		print(f"[FILE] Image saved to {STILLS}cam0_{fname}")
	else:
		print("[ERROR] Camera 0 not found")

	if cam1 is not None:
		cam1.switch_mode_and_capture_file(capture_config, STILLS+"cam1_"+fname)
		print(f"[FILE] Image saved to {STILLS}cam1_{fname}")
	else:
		print("[ERROR] Camera 1 not found")
	print_cam_info(capture_config)
	


## ==========[ AUDIO FUNCTIONS ]========== ##
# Initialize Mic
def start_microphone():
	global DEVICE, SAMPLE_RATE
	mic = PyAudio()
	DEVICE = int(mic.get_default_input_device_info()['index'])
	SAMPLE_RATE = int(mic.get_device_info_by_index(DEVICE)['defaultSampleRate'])
	return mic


# Record Audio
def record_audio():
	global frames, stream, info
	# Initialize PyAudio
	fname = strftime("%Y-%m-%d_%H-%M-%S")
	stream = mic.open(format = paInt16, channels = CHANNELS, rate = SAMPLE_RATE, input_device_index = DEVICE, input = True)
	sleep(0.00868)

	# Get Audio Data
	print("[INFO] Recording Started")
	frames = []
	while button.is_pressed:
		print("*", end="", flush=True)
		# frames.append(stream.read(CHUNK, exception_on_overflow=False))
		frames.append(np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16))
		sleep(0.00868)
	frames = np.hstack(frames)
	# Stop Recording
	stream.stop_stream()
	print()
	print("[INFO] Recording Stopped")
	print(f"\t[INFO] Recording Duration: {len(frames)/SAMPLE_RATE:.2f} seconds")
	# Save Recording
	save_audio(fname, frames)
	frames = None
	info = True

	  
# Save Recording
def save_audio(fname, frames):
	# Save Recording
	print(f"[INFO] Saving Audio...")
	with wave.open(RECORDINGS + f"{fname}.wav", "wb") as f:
		f.setnchannels(CHANNELS)
		f.setsampwidth(mic.get_sample_size(paInt16))
		f.setframerate(SAMPLE_RATE)
		f.writeframes(frames)
	print(f"[FILE] Audio saved to {RECORDINGS}{fname}")
	print(f"\t[INFO] File Size: {os.path.getsize(RECORDINGS+fname+'.wav')/1024:.2f} KB")
	  

## ==========[ BUTTON EVENTS ]========== ##
def setup_button():
	global button
	button = Button(BUTTON_PIN, bounce_time=0.5)
	button.when_held = on_button_press
	button.hold_time = 0.5
	button.hold_repeat = False
	button.when_released = on_button_release


# Button Press Event
def on_button_press():
	take_picture()
	record_audio()

# Button Release Event
def on_button_release():
	do_nothing()

# Terminate
def terminate():
	if stream:
		stream.stop_stream()
		stream.close()
	stop_camera(cam0)
	stop_camera(cam1)
	mic.terminate()
	print("[INFO] Terminated all processes")
	exit(0)


## ==========[ MAIN FUNCTION ]========== ##
def main():
	global cam0, cam1, mic, button, frames, stream, info
	
	# Setup Button
	setup_button()
	# Start Cameras
	cam0 = start_camera(0, control0, preview=False)
	cam1 = start_camera(1, control1, preview=False)
	# Start Microphone
	mic = start_microphone()

	try:
		while True:
			sleep(0.5)
			if frames is None and info:
				info = False
				print("\n\n[READY] Press Button to Take a Picture & Record Audio | [CTRL+C] to Exit")
	except KeyboardInterrupt:
		print("Exiting...")
		terminate()


## ==========[ DRIVER ]========== ##
if __name__ == "__main__":
	main()