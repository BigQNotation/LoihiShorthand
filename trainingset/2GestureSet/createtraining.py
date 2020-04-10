from tkinter import *
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from queue import Queue
import datetime

import csv
import os
from tempfile import TemporaryFile
import glob
import cv2

# save image and label to numpy binary files
label_swapper = 0
image_array = []
label_array = []
#files = glob.glob('./*.PNG')
files = sorted(glob.glob('./*.png'))
for myFile in files:
    image = cv2.imread(myFile)
    print(myFile)
    dim = 20,20
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    resized_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    image_array.append(resized_gray)
    label_array.append(label_swapper % 2) # change mod to match amount of gestures to be trained
    label_swapper = label_swapper + 1
np.save('./imageTrain',image_array)
np.save('./labelTrain',label_array)
