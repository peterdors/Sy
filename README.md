# Sy
Sy: The face tracking robot built using OpenCV for Python and the servoblaster repo. 

Sy will move left, right, up, and down to follow your face!

Sy was built on two servos, a raspberry pi, and an old school Logitech webcam, along with the necessary hardware and jumper wires for putting everything together.

Currently Sy only uses the haarcascade frontal face file for facial recognition, and will only track one face in the frame at a time. If there are multiple faces in the frame, it will only detect the first face found and track it (it may change the sequence of faces found, so a different face may be tracked each time but again this is only if multiple faces are in the frame at once).

References That Helped Me Complete This Project. 

* Instructable that guided me through the hardware build and some coding ideas.
	https://www.instructables.com/id/Pan-Tilt-face-tracking-with-the-raspberry-pi/

* PyImageSearch article that aided with further code implementation.
	https://www.pyimagesearch.com/2019/04/01/pan-tilt-face-tracking-with-a-raspberry-pi-and-opencv/

* Instructable that helped me take my first steps at servo motor controlling. 
	https://www.instructables.com/id/Servo-Motor-Control-With-Raspberry-Pi/

* This problem & solution helped me with figuring out how to stop a Ctrl+C Traceback error.
	https://stackoverflow.com/questions/11312525/catch-ctrlc-sigint-and-exit-multiprocesses-gracefully-in-python

* PiBits repo that provided the ServoBlaster C library for use. 
	https://github.com/richardghirst/PiBits/tree/master/ServoBlaster
