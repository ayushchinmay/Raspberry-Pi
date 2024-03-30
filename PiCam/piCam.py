"""
    AUTHOR      :   Ayush Chinmay, Vigneshwer Ramamoorthi
    DATE CREATED:   29 Mar 2024

    DESCRIPTION :   Python code to capture image using Raspberry Pi Camera Module V2

    COMPONENTS:
            - Raspberry Pi 5    
            - Raspberry Pi Camera Module V2

    ? CHANGELOG ?
        * [29 Mar 2024]
            - [X] Initialization functions for Camera
            - [X] Detect button press, and trigger Image Capture
            - [X] Capture Image and save it to a file
            - [X] Only capture image once -- implement 

    ! TODO !
            - [-] Automagically create Stills directory if it doesn't exist
            - [-] Send Image to an API for processing
"""

## Import Modules
from picamera2 import Picamera2, Preview
from time import sleep, strftime
from gpiozero import Button
import os


# Directory Path
PATH = "/home/ayush-pi/Documents/PyCode/PiCam/Stills/"

if not os.path.exists(PATH):
    os.makedirs(PATH)

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

## Buttons
BUTTON_PIN = 2
button = Button(BUTTON_PIN)

def print_info(data):
    print("    {")
    for key in data:
        print(f"\t{key}: {data[key]}")
    print("    }")


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
        cam.start_preview(Preview.QTGL, x=100, width=820, height=616)
    else:
        cam.start_preview(Preview.NULL)
    cam.start()
    print(f"\n[CAM {camnum}]")
    print("    Config: ")
    print_info(preview_config)
    print("    Controls: ")
    print_info(controls)
    return cam


# Stop Camera function
def stop_camera(cam):
    cam.close()
    print("[INFO] Camera Stopped")


# Take Picture function
def take_picture():
    print("[INFO] Taking Picture in 3 seconds...")
    sleep(3)
    fname = f"image_{strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    cam0.switch_mode_and_capture_file(capture_config, PATH+"cam0_"+fname)
    cam1.switch_mode_and_capture_file(capture_config, PATH+"cam1_"+fname)
    print("[INFO] Switching to Capture Mode: ")
    print_info(capture_config)
    print(f"[FILE] Image saved to {PATH}cam0_{fname}")
    print(f"[FILE] Image saved to {PATH}cam1_{fname}")
    

def do_nothing():
    sleep(3)


def main():
    global cam0, cam1

    button.when_pressed = take_picture
    button.when_released = do_nothing


    cam0 = start_camera(0, control0, preview=False)
    cam1 = start_camera(1, control1, preview=False)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        stop_camera(cam0)
        stop_camera(cam1)


if __name__ == '__main__':
    main()