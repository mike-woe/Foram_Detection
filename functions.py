# Functions to be called by GUIDetect_Blob_Count.py

# Import necessary modules
import serial
import time
from datetime import datetime
import cv2
import numpy as np
import _thread
from camera import *


#########################################################################################################
# Open Serial Communications with Arduino
def Open_Comms():
    # Note: port is dependent upon specific Arduino and may need to be changed as necessary 
    arduino = serial.Serial(port='com6',baudrate=9600,timeout=.1)
    time.sleep(2)
    return arduino

#########################################################################################################
# Turn pressure box off
def Solenoids_Off(arduino):
    arduino.write(str.encode('0'))
    time.sleep(1)
    arduino.close()

###################################################################################################################

def Solenoid_State(title, arduino, state):
    arduino.write(str.encode(str(state)))

################################################################################

def Awaiting_Foram(arduino):
    arduino.write(str.encode('1'))  # Gate 1 open, gate 2 closed
    ready = True                    # Set and return flags
    detected = False
    return ready, detected

########################################################################################################

def Foram_Found(arduino, i, image, folder, cam):
    global ready2
    
    _thread.start_new_thread(Solenoid_State, ("New State", arduino, 3,))
    
    ready2 = False
    
    _thread.start_new_thread(timer, ("Timing",))
    
    while not ready2:
        image = cam.get_pil_image()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (1200, 700))
        image = image[10:600, 250:1000]
        cv2.imshow('Forams', image)
        key = cv2.waitKey(1)
        if key == 27:  # Escape key pressed
            break

    now = datetime.now()
    cv2.imwrite(folder + "\\" + "foram" + now.strftime("%H-%M-%S") + '.png', image)

    _thread.start_new_thread(Solenoid_State, ("New State", arduino, 2,))

    ready2 = False   # Set flag
    _thread.start_new_thread(timer, ("Timing",))
    while not ready2:
        image = cam.get_pil_image()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (1200, 700))
        image = image[10:600, 250:1000]
        cv2.imshow('Forams', image)
        key = cv2.waitKey(1)
        if key == 27:  # Escape key pressed
            break

    _thread.start_new_thread(Solenoid_State, ("New State", arduino, 1,))
    ready2 = False
    _thread.start_new_thread(timer, ("Timing",))

    while not ready2:
       image = cam.get_pil_image()
       image = np.array(image)
       image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
       image = cv2.resize(image, (1200, 700))
       image = image[10:600, 250:1000]
       cv2.imshow('Forams', image)
       key = cv2.waitKey(1)
       if key == 27:  # Escape key pressed
           break
    ready = False
    return ready, i

########################################################################################################

def Blob_Detect(image, clean_image):

    detected = False
    
    # Set up the SimpleBlobDetector with default parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 100  # Changed from 50 to 100
    params.maxThreshold = 256

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 1_000  # Changed from 1_000 to 5_000
    
    params.maxArea = 100_000 # Uncommented and changed from 10_000 to 100_000

    # Filter by Color (black=0)
    params.filterByColor = True
    params.blobColor = 255

    # Filter by Circularity
    params.filterByCircularity = False

    # Filter by Convexity
    params.filterByConvexity = False

    # Filter by InertiaRatio
    params.filterByInertia = False

    # Distance Between Blobs
    params.minDistBetweenBlobs = 0

    # Do detecting
    detector = cv2.SimpleBlobDetector_create(params)

    # find key points for blob detection
    keypoints = detector.detect(image)


    if keypoints:
        detected = True

    # create black screen on which shapes are drawn
    blank = np.zeros((1,1))

    blobs = cv2.drawKeypoints(clean_image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Get the number of blobs currently detected
    blob_num = (len(keypoints))

    return blobs, detected, blob_num

###################################################################################################################

def show():
    global myLabel
    #cam.set_auto_exposure(var.get())
    if var.get() == "On":
        cam.set_auto_exposure(True)
    else:
        cam.set_auto_exposure(False)
    myLabel = Label(root, text=var.get())
    myLabel.grid(row=0, column=2)

###############################################################################

def timer(a):
    global ready2
    time.sleep(3)
    ready2 = True

