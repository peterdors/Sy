import os, cv2
import RPi.GPIO as GPIO
import constants as const

from time import sleep
from motor import Motor
from servoblaster import ServoBlaster

# Method for labeling the detected image.
# Utilizes saving detected facial images function (cv2.write)
def label_detected_image(detectedImage, frame, text):
    font                   = const.FONT
    fontScale              = 1
    fontColor              = (0,0,0)
    lineType               = 2
    count = 0

    # Only one detected face will be outlined.
    x, y, w, h = detectedImage[0]
    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(
        frame,
        text,
        (x, y-const.ADJUST_TEXT_PUT),
        font,
        fontScale,
        fontColor,
        lineType
        )

# CONSTANTS
# ==========
# File path to the haar cascade file.
CASCADE_FILE = 'haarcascades/haarcascade_frontalface_default.xml'

# Offsets are used to allow some leeway when determining if the face is centered
# in the frame or not. 
OFFSET_PAN = 100
OFFSET_TILT = 100
TILT_ADJ = 10
PAN_ADJ = 10
SERVO_RANGE = (0, 250)

# PRESETS
# ========
face = [0,0,0,0]
fface = [0,0,0,0]
center_face = [0,0]
x = y = w = h = 0

# Initialize webcam with default width and height dimensions.
webcam = cv2.VideoCapture(-1)        
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, const.FRAME_WIDTH)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, const.FRAME_HEIGHT)
frame = None

# Values for determining which way to move the panoramic servo. 
left = const.FRAME_WIDTH / 2 - OFFSET_PAN # 640 / 2 + 100 = 520
right = const.FRAME_WIDTH / 2 + OFFSET_PAN # 640 / 2 - 100 = 220
top = const.FRAME_HEIGHT / 2 + OFFSET_TILT # 480 / 2 + 100 = 340
bottom = const.FRAME_HEIGHT / 2 - OFFSET_TILT # 480 / 2 - 100 = 140

pan_motor_id = 'P1-7'
tilt_motor_id = 'P1-11'

# Frontal face pattern detection.
frontal_face = cv2.CascadeClassifier(CASCADE_FILE)

# Initialize the servo motors. 
sb = ServoBlaster()

# Let everything warm up.
sleep(2)

# Preset the angle of the servos. We have to get the servos to move in order 
# for them to respond during face movements.  
sb.set_angle(pan_motor_id, 250)
sb.set_angle(pan_motor_id, -120)
sb.set_angle(tilt_motor_id, 250)
sb.set_angle(tilt_motor_id, -120)

# Main loop for face detection and tracking.
while True:
	face_found = False
	if not face_found: 
		# Get the frame from the webcam. Grab 5 frames per iteration to get
		# realtime image using raspberry pi.  
		frame = webcam.read()[1]
		frame = webcam.read()[1]
		frame = webcam.read()[1]
		frame = webcam.read()[1]
		frame = webcam.read()[1]

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
		# Run face detection in the frame.
		face = frontal_face.detectMultiScale(
	                gray,
	                scaleFactor=const.SCALE_FACTOR,
	                minNeighbors=const.MIN_NEIGHBORS,
	                minSize=(const.MIN_SIZE, const.MIN_SIZE),
	                flags=const.FLAGS
	        )		
		

		# Check if a face was found in the frame.
		if (len(face) >= 1):
			label_detected_image(face, frame, '')
			face_found = True
			fface = face[0]
	
	if not face_found: 
		# Reset frontal face and center face values to zeroes if face wasn't found.
		fface = [0,0,0,0]
		center_face = [0,0]
	else: 
		# Calculate the center position of the detected face if face was found.
		x,y,w,h = fface
		center_face = [w/2 + x, h/2 + y]

	cv2.imshow('', frame)

	if (cv2.waitKey(1) & 0xFF == ord('q')): 
		break

	# If a face was not detected, the values in center_face will be zero.
	# Continue iterating until we find a face in the frame. 
	if center_face[0] == 0:
		continue

	# NOTES ON SERVO MOTOR MOVEMENTS
	# ==========================================================================
	# Servo motor moves as expected on the pan, but some slight errors 
	# on the tilt motor. 
	# Also have an issue where the pan motor won't move until the person
	# face is all the way to the right, then the motor will abruptly move 
	# right and have to be physically moved again. Similar situation with the 
	# tilt motor occurs, but it will abruptly move up all the way and have to be 
	# guided back to original position. 
	# ==========================================================================

	# PAN MOTOR MOVEMENTS
	# Do stuff to evaluate and pan the camera to track the face.
	if int(center_face[0]) >= int(right):
		print('Center Face from Right: {}'.format(center_face[0]))
		sb.set_angle(pan_motor_id, PAN_ADJ * -1) # move motor left
		
	elif int(center_face[0]) <= int(left):
		print('Center Face from Left: {}'.format(center_face[0]))
		sb.set_angle(pan_motor_id, PAN_ADJ) # move motor right

	# TILT MOTOR MOVEMENTS
	# Do stuff to evaluate and tilt the camera to track the face.
	# Have to test which direction servo motor will move based on hardware
	# setup.
	if int(center_face[1]) > int(top):
		print('Center Face from Top: {}'.format(center_face[1]))
		sb.set_angle(tilt_motor_id , TILT_ADJ) # move motor up
		
	elif int(center_face[1]) < int(bottom):
		print('Center Face from Bottom: {}'.format(center_face[1]))
		sb.set_angle(tilt_motor_id, TILT_ADJ * -1) # move motor down
		
# Cleanup. :)
webcam.release()
cv2.destroyAllWindows()
