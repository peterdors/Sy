# Rewrite of the main.py file for Sy. 
# The goal here is to incorporate threads/processes for face tracking. 
import os, cv2, signal, sys
import constants as const
from time import sleep
from servoblaster import ServoBlaster
from multiprocessing import Manager, Process

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

# Values for determining which way to move the panoramic servo. 
left = const.FRAME_WIDTH / 2 - OFFSET_PAN # 640 / 2 + 100 = 520
right = const.FRAME_WIDTH / 2 + OFFSET_PAN # 640 / 2 - 100 = 220
top = const.FRAME_HEIGHT / 2 + OFFSET_TILT # 480 / 2 + 100 = 340
bottom = const.FRAME_HEIGHT / 2 - OFFSET_TILT # 480 / 2 - 100 = 140

# Servo motor id's 
pan_motor_id = 'P1-7'
tilt_motor_id = 'P1-11'

# Initialize the servo motors. 
sb = ServoBlaster()

# Preset the angle of the servos. We have to get the servos to move in order 
# for them to respond during face movements.  
# sb.set_angle(pan_motor_id, 250)
# sb.set_angle(pan_motor_id, -120)
# sb.set_angle(tilt_motor_id, -250)
# sb.set_angle(tilt_motor_id, 80)

# Let everything warm up.
sleep(2)

# Function to handle keyboard interrupt.
def signal_handler(sig, frame):
	# Print a status message and exit the program.
	print("[INFO] You pressed `ctrl + c`! Exiting...")

	sys.exit()

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


def obj_center(objX, objY):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	webcam = cv2.VideoCapture(-1)        
	webcam.set(cv2.CAP_PROP_FRAME_WIDTH, const.FRAME_WIDTH)
	webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, const.FRAME_HEIGHT)

	sleep(1.0) # warm up

	# Frontal face pattern detection.
	frontal_face = cv2.CascadeClassifier(CASCADE_FILE)

	while True:
		face_found = False
		if not face_found: 
			# Get the frame from the webcam. Grab 5 frames per iteration to get
			# realtime image using raspberry pi.  
			for _ in range(5): 
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
			if (len(face) > 0):
				label_detected_image(face, frame, '')
				face_found = True
				fface = face[0]
		
		if not face_found: 
			# Reset frontal face and center face values to zeroes if face wasn't found.
			fface = [0,0,0,0]
			center_face = [0,0]
			objX.value = const.FRAME_WIDTH // 2
			objY.value = const.FRAME_HEIGHT // 2
		else: 
			# Calculate the center position of the detected face if face was found.
			x,y,w,h = fface
			center_face = [w/2 + x, h/2 + y]
			objX.value = center_face[0]
			objY.value = center_face[1]

		cv2.imshow('', frame)

		if (cv2.waitKey(1) & 0xFF == ord('q')): 
			break


	# Cleanup. :)
	webcam.release()
	cv2.destroyAllWindows()

	return



def go(sb, objX, objY):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	while True: # loop indefinitely

		if (objX.value == 0 and objY.value == 0):
			continue

		# PAN MOTOR MOVEMENTS
		# Do stuff to evaluate and pan the camera to track the face.
		if int(objX.value) < int(left - 60):
			print('Object from left: {}'.format(objX.value))
			sb.set_angle(pan_motor_id, PAN_ADJ + 10) # move motor left
		elif int(objX.value) < int(left):
			print('Object from left: {}'.format(objX.value))
			sb.set_angle(pan_motor_id, PAN_ADJ) # move motor left

		elif (int(objX.value) > int(right + 60)):
			print('Object from right: {}'.format(objX.value))
			sb.set_angle(pan_motor_id, (PAN_ADJ + 10) * -1) # move motor right
		elif (int(objX.value) > int(right)):
			print('Object from right: {}'.format(objX.value))
			sb.set_angle(pan_motor_id, PAN_ADJ * -1) # move motor right

		# TILT MOTOR MOVEMENTS
		# Do stuff to evaluate and tilt the camera to track the face.
		if int(objY.value) > int(top + 60):
			print('Object from top: {}'.format(objY.value))
			sb.set_angle(tilt_motor_id , TILT_ADJ + 10) # move motor up
		elif int(objY.value) > int(top):
			print('Object from top: {}'.format(objY.value))
			sb.set_angle(tilt_motor_id , TILT_ADJ) # move motor up
	
		elif int(objY.value) < int(bottom - 60):			
			print('Object from bottom: {}'.format(objY.value))
			sb.set_angle(tilt_motor_id, (TILT_ADJ + 10) * -1) # move motor down
		elif int(objY.value) < int(bottom):			
			print('Object from bottom: {}'.format(objY.value))
			sb.set_angle(tilt_motor_id, TILT_ADJ * -1) # move motor down

		sleep(0.4)

if __name__ == "__main__":

	with Manager() as manager:	

		# Set integer values for the object's (x, y)-coordinates.
		objX = manager.Value("i", 0)
		objY = manager.Value("i", 0)

		# Pan and tilt values will be managed by distance the face is from 
		# the center, but this is to be used later. 
		pan = manager.Value("i", 0)
		tlt = manager.Value("i", 0)

		processObjectCenter = Process(target=obj_center, 
									args=(objX, objY))
		processSetServos = Process(target=go, args=(sb, objX, objY))

		processObjectCenter.start()
		processSetServos.start()

		processObjectCenter.join()
		processSetServos.join()





