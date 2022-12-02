from camera import *
import numpy as np
import cv2
import _thread
import time
import datetime
import os
from datetime import datetime
from skimage.filters import median
from skimage.morphology import disk
from tkinter import *
from PIL import ImageTk, Image
from camera import *
from functions import *

# Create folder to store images
folder = "images\\" + datetime.today().strftime("%m-%d-%Y")
if not os.path.isdir('images'):
    os.mkdir('images')
if not os.path.isdir(folder):
    os.mkdir(folder)
    
###############################################################################
def close():
    global arduino, running
    running = False
    time.sleep(.2)
    Solenoids_Off(arduino)
    cv2.destroyAllWindows()
    root.destroy()
##############################################################################    
# Main loop
def playing(Title):
    global ready2, running
    ready = True  # Set and return flags
    detected = False

    previous_blobs=0

    global i, cam
    while running:
        # Convert image from PIL to cv2
        image = cam.get_pil_image()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Resize image
        image = cv2.resize(image, (1200, 700))
        image = image[10:600, 250:1000]
        if ready:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            median_blur_image = median(gray_image, disk(3), mode='constant', cval=0.0)            
            blobs, detected, number_of_blobs = Blob_Detect(median_blur_image, image)
            
        cv2.imshow('Forams', blobs)
        
        key = cv2.waitKey(1)
        if key == 27:  # Escape key pressed
            break
        
        if (previous_blobs < number_of_blobs) and (detected == True) and ready:
            ready = Foram_Found(arduino, i, image, folder, cam)
            print(number_of_blobs)

            # If no forams in frame, reset flags
        else:
            ready, detected = Awaiting_Foram(arduino)

        previous_blobs = number_of_blobs

# Open AmScope camera
cam = ToupCamCamera()
cam.open()
time.sleep(1)
#===================================================
running = True
#====================================================
# Set default values for certain parameters
cam.set_gamma(180)
cam.set_gain(100)
cam.set_contrast(100)

# Create GUI window
root = Tk()
root.title("Microscope Interface")
root.geometry("200x500")


arduino = Open_Comms()
i = 0

_thread.start_new_thread(playing, ("playing", ))


def slide(position):
    global gamma, gain, brightness, contrast, hue, saturation, exposure_time, cam

    #display accuracy
    lgamma = Label(root, text="Gamma:   " + str(gamma.get())).grid(row=2, column=0)
    lgain = Label(root, text="Gain:   " + str(gain.get())).grid(row=4, column=0)
    lbrightness = Label(root, text="Brightness:   " + str(brightness.get())).grid(row=6, column=0)
    lcontrast= Label(root, text="Contrast:   " + str(contrast.get())).grid(row=8, column=0)
    lhue = Label(root, text="Hue:   " + str(hue.get())).grid(row=10, column=0)
    lsaturation = Label(root, text="Saturation:   " + str(saturation.get())).grid(row=12, column=0)
    lexposure_time = Label(root, text="Exposure Time:   " + str(exposure_time.get())).grid(row=14, column=0)

    #switch to setting value first, then set labels to cam.get_value()

    #actually set values for microscope while changing
    cam.set_gamma(gamma.get())
    cam.set_gain(gain.get())
    cam.set_brightness(brightness.get())
    cam.set_contrast(contrast.get())
    cam.set_hue(hue.get())
    cam.set_saturation(saturation.get())
    cam.set_exposure_time(exposure_time.get())

# Create Sliders
gamma = Scale(root, from_=20, to=180, orient=HORIZONTAL, command=slide)
gain = Scale(root, from_=100, to=300, orient=HORIZONTAL, command=slide)
brightness = Scale(root, from_=-64, to=64, orient=HORIZONTAL, command=slide)
contrast = Scale(root, from_=-100, to=100, orient=HORIZONTAL, command=slide)
hue = Scale(root, from_=-180, to=180, orient=HORIZONTAL, command=slide)
saturation = Scale(root, from_=0, to=255, orient=HORIZONTAL, command=slide)
exposure_time = Scale(root, from_=0, to=255, orient=HORIZONTAL, command=slide)

# Set default parameters
gamma.set(180)
gain.set(100)
brightness.set(cam.get_brightness())
contrast.set(100)
hue.set(cam.get_hue())
saturation.set(cam.get_saturation())
exposure_time.set(cam.get_exposure_time())

# add Exit menu item
button_quit = Button(root, text="Quit", command=close)
button_quit.grid(row=15, column=0)

# Position Sliders
gamma.grid(row=1, column=0)
gain.grid(row=3, column=0)
brightness.grid(row=5, column=0)
contrast.grid(row=7, column=0)
hue.grid(row=9, column=0)
saturation.grid(row=11, column=0)
exposure_time.grid(row=13, column=0)

# Create and Place Slider Labels
lgamma = Label(root, text="Gamma:   " + str(gamma.get())).grid(row=2, column=0)
lgain = Label(root, text="Gain:   " + str(gain.get())).grid(row=4, column=0)
lbrightness = Label(root, text="Brightness:   " + str(brightness.get())).grid(row=6, column=0)
lcontrast = Label(root, text="Contrast:   " + str(contrast.get())).grid(row=8, column=0)
lhue = Label(root, text="Hue:   " + str(hue.get())).grid(row=10, column=0)
lsaturation = Label(root, text="Saturation:   " + str(saturation.get())).grid(row=12, column=0)
lexposure_time = Label(root, text="Exposure Time:   " + str(exposure_time.get())).grid(row=14, column=0)

# Creating text document of all parameters to be stored with images
start_time = datetime.now()

with open(folder + "\\parameters_used.text", "w+") as f:
    f.write("Start time: " + str(start_time) + "\n")
    f.write("Camera Parameters:\n")
    f.write("Gamma: " + str(gamma.get()) + "\n")
    f.write("Gain: " + str(gain.get()) + "\n")
    f.write("Brightness: " + str(brightness.get()) + "\n")
    f.write("Contrast: " + str(contrast.get()) + "\n")
    f.write("Hue: " + str(hue.get()) + "\n")
    f.write("Saturation: " + str(saturation.get()) + "\n")
    f.write("Exposure time: " + str(exposure_time.get()) + "\n\n")

##imcount = Label(root, text=i)
##imcount.grid(row=0, column=6)

root.mainloop()
