#!/usr/bin/python3
"""
    AUTHOR          : Ayush Chinmay
    DATE CREATED    : 29 Mar 2024

    DESCRIPTION     : Python code to capture image using Raspberry Pi Camera Module V2 upon smile detection

    COMPONENTS:
            - Raspberry Pi 5    
            - Raspberry Pi Camera Module V2

    ? CHANGELOG ?
        * [29 Mar 2024]
            - [X] Initialization functions for Camera
            - [X] Detect smile
        * [30 Mar 2024]
            - [X] Trigger Image Capture upon smile detection
            - [X] Capture Image and save it to a file
            
    ! TODO !
            - [-] ...
"""


## ==========[ IMPORTS ]========== ##
import cv2
import numpy as np
from picamera2 import Picamera2
from time import strftime, sleep, time

## ==========[ CONSTANTS ]========== ##
# Directory Path
PATH = "/home/ayush-pi/Documents/PyCode/PiCam/Stills/"  # Directory Path

# Camera
CAM = 1
WIDTH = 640
HEIGHT = 480
SMILE_DURATION = 3

# Colors
chex = ["f44a4a", "fb8f23", "fee440", "7aff60", "00f5d4", "00bbf9", "9b5de5", "f15bb5"]

## ==========[ GLOBALS ]========== ##
colors = None
smile_start_time = None
picam2 = None
capture_config = None

# Cascade Classifiers
face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
smile_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_smile.xml")


## ==========[ HELPERS ]========== ##
# Convert Hex to BGR
def hex2bgr(str):
    if str[0] == '#':
        str = str[1:]
    return tuple((int(str[4:6],16), int(str[2:4],16), int(str[0:2],16)))


# Check if a rectangle is inside another
def is_inside(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if x1 >= x2 and y1 >= y2 and x1 + w1 <= x2 + w2 and y1 + h1 <= y2 + h2:
        return True
    return False


# Capture Image
def capture_image():
    global picam2, capture_config
    fname = f"{PATH}smile_{strftime('%Y-%m-%d_%H-%M-%S')}.png"
    print(f"[INFO] Capturing Image: {fname}")
    picam2.switch_mode_and_capture_file(capture_config, fname)
    sleep(1)


## ==========[ MAIN ]========== ##
def main():
    global colors, smile_start_time, picam2, capture_config
    colors = [hex2bgr(i) for i in chex]

    # Start Camera
    cv2.startWindowThread()

    picam2 = Picamera2(camera_num=CAM)
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (WIDTH, HEIGHT)}, display="main"))
    picam2.set_controls({"AwbEnable": True, "AeEnable": True, "NoiseReductionMode": 2})
    capture_config = picam2.create_still_configuration()
    picam2.start()

    while True:
        im = picam2.capture_array()

        grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(grey, 1.1, 3)
        smiles = smile_detector.detectMultiScale(grey, 1.6, 12)
        
        print(f"[RUNNING] Looking for Smiles...")

        for (xf, yf, wf, hf) in faces:
            cv2.rectangle(im, (xf, yf), (xf + wf, yf + hf), colors[0])

            for (x, y, w, h) in smiles:
                if is_inside((x, y, w, h), (xf, yf, wf, hf)):
                    cv2.rectangle(im, (x, y), (x + w, y + h), colors[1])
                else:
                    smiles = np.delete(smiles, 0, 0)
                    continue
            
            if len(smiles) > 0:
                if smile_start_time is None:
                    smile_start_time = time()
                else:
                    if time() - smile_start_time > SMILE_DURATION:
                        print("[INFO] Smile Detected!")
                        capture_image()
                        smile_start_time = None
            else:
                smile_start_time = None
        
        # print(f"Faces: {len(faces)} | Smiles: {len(smiles)}")

        cv2.imshow("Camera", im)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()