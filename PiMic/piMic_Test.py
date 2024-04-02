from pyaudio import PyAudio, paInt16
import wave
from time import sleep, strftime
import matplotlib.pyplot as plt
import numpy as np
import os


## Constants
PATH = "/home/ayush-pi/Documents/PyCode/PiMic/Tests/"

try :
	os.makedirs(PATH)
except:
	pass

# Constants
CHANNELS = 1
RATE = 44100
CHUNK = 4096
RECORD_SECONDS = 1
DEVICE = 11

colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5"]

def show_devices():
	p = PyAudio()
	for i in range(p.get_device_count()):
		dev = p.get_device_info_by_index(i)
		print((i,dev['name'],dev['maxInputChannels']))
	print(p.get_default_input_device_info())
# (0, 'USB PnP Sound Device: Audio (hw:0,0)', 1)


def main():
	# Initialize PyAudio
	fname = strftime("%Y-%m-%d_%H-%M-%S")
	mic = PyAudio()
	stream = mic.open(format = paInt16, channels = CHANNELS, rate = RATE, input_device_index = DEVICE, input = True)

	print("Recording")
	sleep(RECORD_SECONDS)

	# Get Audio Data
	frames = []
	for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
		frames.append(stream.read(CHUNK, exception_on_overflow=False))
		sleep(0.00868)

	# Stop Recording
	stream.stop_stream()
	# Close PyAudio
	stream.close()

	print("Done Recording")

	# Save Recording
	with wave.open(PATH + f"{fname}.wav", "wb") as f:
		f.setnchannels(CHANNELS)
		f.setsampwidth(mic.get_sample_size(paInt16))
		f.setframerate(RATE)
		f.writeframes(b''.join(frames))

	# Plot Audio Data
	fig = plt.figure(figsize=(12, 4), dpi=150)
	signal = np.frombuffer(b''.join(frames), dtype=np.int16)
	ax = fig.add_subplot(111)
	ax.plot(signal, color=colors[1])
	ax.set_xlim([0, len(signal)])
	ax.set_title(f"Audio Signal: {CHUNK} | {fname}")
	ax.set_xlabel("Bit")
	ax.set_ylabel("Amplitude")
	plt.tight_layout()
	plt.savefig(PATH + f"{fname}.png")
	# plt.show()


if __name__ == "__main__":
	show_devices()
	main()
	# for i in range(5):
	# 	CHUNK = 512 * 2**i
	# 	main()
