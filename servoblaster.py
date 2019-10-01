# ServoBlaster.py
# ================
# ServoBlaster class initializes the servoblaster API installed on our system. 
# The class is initialized by identifying the number of servos used, and each 
# servo has an ID they are associated with. For now we are working with two 
# servos so the id's will be: 'P1-7' & '(to be used)'
# 
# NOTE: PWM will be between 0 and 250 for the micro-servos we are using. 
from time import sleep

class ServoBlaster(object):
	"""docstring for ServoBlaster"""
	def __init__(self):
		# Open the file to write to servoblaster input. 
		self.servoblaster = open('/dev/servoblaster', 'w')

	def set_angle(self, servo_id, val):
		# This conditional statement is only for formatting purposes when we 
		# write to servoblaster. 
		print('Sending value: {}'.format(val))

		if (val > 0):
			self.servoblaster.write('{}=+{}\n'.format(servo_id, val))
		else:
			self.servoblaster.write('{}={}\n'.format(servo_id, val))

		self.servoblaster.flush()


		
