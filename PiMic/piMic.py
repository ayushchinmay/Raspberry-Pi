"""
    AUTHOR      :   Ayush Chinmay
    DATE CREATED:   01 Apr 2024

    DESCRIPTION :   Python code to capture audio on button press

    COMPONENTS:
            - Raspberry Pi 5 ()
            - Microphone
			- Button

    ? CHANGELOG ?
        * [01 Apr 2024]
            - [X] Initialization functions for Microphone
            - [X] Detect button press
            - [X] Record Audio on button press
            - [X] Stop Recording on button release
            - [X] Save Audio to a file
			- [X] Plot Audio Data

    ! TODO !
            - [ ] Send Audio to an API for processing
            - [ ] Receive API response and display it on the screen
"""

## ==========[ MODULES ]========== ##
import os
from gpiozero import Button
from time import sleep, strftime
from pyaudio import PyAudio, paInt16
import wave
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


## ==========[ CONSTANTS ]========== ##
# Path to save recordings
PATH = "/home/ayush-pi/Documents/PyCode/PiMic/"

try:
    os.makedirs(PATH+"/Recordings/")
    os.makedirs(PATH+"/Waveforms/")
except:
    pass

# Colors for plotting
colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5"]

# Button
BUTTON_PIN = 26
button = Button(BUTTON_PIN)

# Initialize PyAudio
mic = PyAudio()
DEVICE = int(mic.get_default_input_device_info()['index'])
SAMPLE_RATE = int(mic.get_device_info_by_index(DEVICE)['defaultSampleRate'])
CHANNELS = 1    # int(mic.get_device_info_by_index(DEVICE)['maxInputChannels'])
CHUNK = 4096
FORMAT = paInt16

frames = None
stream = None
info = True

## ==========[ FUNCTIONS ]========== ##
# Show available devices
def show_devices():
	p = PyAudio()
	for i in range(p.get_device_count()):
		dev = p.get_device_info_by_index(i)
		print((i,dev['name'],dev['maxInputChannels']))
	print(p.get_default_input_device_info())
# (0, 'USB PnP Sound Device: Audio (hw:0,0)', 1)

# Record Audio
def record():
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
	save(fname, frames)
	plot(fname, frames)
	frames = None
	info = True


# Save Recording
def save(fname, frames):
	# Save Recording
	print(f"[INFO] Saving Audio...")
	with wave.open(PATH + f"Recordings/{fname}.wav", "wb") as f:
		f.setnchannels(CHANNELS)
		f.setsampwidth(mic.get_sample_size(paInt16))
		f.setframerate(SAMPLE_RATE)
		f.writeframes(frames)
	print(f"[FILE] Audio saved to {PATH}Recordings/{fname}")
	print(f"\t[INFO] File Size: {os.path.getsize(PATH+'Recordings/'+fname+'.wav')/1024:.2f} KB")


# Plot Audio Data
def plot(fname, frames):
	# Plot Audio Data
	fig = plt.figure(figsize=(12, 4), dpi=150)
	fig.suptitle("CHUNK = 4096 | SAMPLE_RATE = 44100 Hz")
	ax = fig.add_subplot(111)
	ax.plot(frames, color=colors[2])
	ax.set_xlim([0, len(frames)])
	ax.set_title(f"Waveform: {fname}.wav", fontdict={"fontsize": 16, "color": colors[1]})
	ax.set_xlabel("Bit")
	ax.set_ylabel("Amplitude")
	plt.tight_layout()
	plt.savefig(PATH + f"Waveforms/{fname}.png")
	print(f"[FILE] Waveform Plot saved to {PATH}Waveforms/{fname}.png")
	# plt.show()


## ==========[ MAIN ]========== ##
def main():
	global info, frames, stream
	# show_devices()
	button.when_pressed = record
	try:
		while True:
			sleep(0.5)
			if frames is None and info:
				info = False
				print("\n\n[READY] Press Button to Start Recording | [CTRL+C] to Exit")

	except KeyboardInterrupt:
		print("Exiting")
		if stream is not None:
			stream.stop_stream()
			stream.close()
			print("[INFO] Stream Closed")
		mic.terminate()
		print("[INFO] Mic Terminated")


## ==========[ DRIVER ]========== ##
if __name__ == "__main__":
	main()
