# Peter Dorsaneo
# Face Tracking Robot
#
# Python script for utilizing constant values throughout the program.
import cv2
import sys
import os

MAX_IMAGES = 20

SCALE_FACTOR = 1.3

MIN_NEIGHBORS = 10

MIN_SIZE = 20

FLAGS = cv2.CASCADE_SCALE_IMAGE

FONT = cv2.FONT_HERSHEY_SIMPLEX

ADJUST_TEXT_PUT = 10

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

WIDTH = 50
HEIGHT = 50

HERTZ = 50

# File path to the haar cascade file.
CASCADE_FILE = 'haarcascades/haarcascade_frontalface_default.xml'

# Offsets are used to allow some leeway when determining if the face is centered
# in the frame or not. 
OFFSET_PAN = 100
OFFSET_TILT = 100
TILT_ADJ = 10
PAN_ADJ = 10
SERVO_RANGE = (0, 250)
        
