"""
    AUTHOR      :   Ayush Chinmay
    DATE CREATED:   26 Mar 2024

    DESCRIPTION :   Python code to capture audio on button press

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
import os
from gpiozero import Button
from time import sleep, time, strftime
from pyaudio import PyAudio, paInt16
import wave
import numpy as np
import matplotlib.pyplot as plt

## Constants
PATH = "/home/ayush-pi/Documents/PyCode/PiMic/"
BUTTON_PIN = 26

colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5"]

# If path does not exist, create it
try:
    os.makedirs(PATH+"/Recordings")
    os.makedirs(PATH+"/Waveforms")
except:
    pass

# Initialize PyAudio
audio = PyAudio()
DEVICE = int(audio.get_default_input_device_info()['index'])
SAMPLE_RATE = int(audio.get_device_info_by_index(DEVICE)['defaultSampleRate'])
CHANNELS = 1    # int(audio.get_device_info_by_index(DEVICE)['maxInputChannels'])
CHUNK = 4096
FORMAT = paInt16

stream = None

# Recording Duration
TIC = time()
# TOC = time()

# Audio File Name
fname = None
asignal = None

# Start Recording
def start_recording():
    global stream, TIC
    stream = audio.open(input_device_index=DEVICE, format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)
    stream.start_stream()
    sleep(0.25)
    TIC = time()
    print("[INFO] Recording Started")

# Stop Recording
def stop_recording():
    global stream, asignal, fname
    if stream is not None:
        TOC = time()
        RECORDING_SECONDS = TOC - TIC

        print("[INFO] Recording Stopped")
        frames = []

        for i in range(0, int(SAMPLE_RATE/CHUNK*RECORDING_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        fname = strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
        wf = wave.open(PATH+'/Recordings/'+fname, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))
        wf.close()
        print(f"[FILE] Audio saved to {PATH}/Recordings/{fname}")

        stream.stop_stream()
        stream.close()
        print("[INFO] Stream Closed")

        asignal = np.frombuffer(b"".join(frames), dtype=np.int16)


# Get Device Info
def show_devices():
    p = PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print((i,dev['name'],dev['maxInputChannels']))
    print(p.get_default_input_device_info())


# Plot Audio Data
def plot_signal(signal, save=False):
    fig = plt.figure(figsize=(10, 4), tight_layout=True)
    ax = fig.add_subplot(111)
    ax.plot(signal, color=colors[0])
    ax.set_title(f"Audio Signal: {fname}")
    ax.set_xlabel("Bit")
    ax.set_ylabel("Data")
    if save:
        plt.savefig(PATH+'/Waveforms/'+fname+".png")
        print(f"[FILE] Image saved to {PATH}/Waveforms/{fname}.png")
    plt.show()


# Button Press Event
button = Button(BUTTON_PIN)

# Main Loop
def main():
    global button, stream, asignal
    button.when_pressed = start_recording
    button.when_released = stop_recording

    try:
        while True:
            sleep(0.5)
            print(".")
            if asignal is not None:
                plot_signal(asignal)
                asignal = None
            else:
                print("[INFO] Ready to Record ...")
    except KeyboardInterrupt:
        print("[INFO] Exiting ...")
        if stream is not None:
            stream.stop_stream()
            stream.close()
        audio.terminate()


if __name__ == '__main__':
    main()