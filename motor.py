# Peter Dorsaneo
#
# motor.py
#
# Class implementation for working with a single servo motor.
# Sets the starting position of the motor,
# the pin used on the Raspberry Pi, and
# the

import RPi.GPIO as GPIO
from time import sleep
import math
import constants as const

def myround(x, prec=1, base=.5):
  return round(base * round(float(x)/base), prec)

def adjust(x):
    r_x = int(x)
    if (x > r_x + 0.5):
        return r_x + 0.5
    else:
        return r_x

class Motor():
    
    # Class member variables.
    hz = const.HERTZ
    pwm = None
    duty = 0
    pin = 0

    # Constructor method.
    def __init__(self, angle=90, pin=3, start=0):
        self.angle = angle
        self.pin = pin
        
        self.set_gpio_mode()
        self.pwm = self.setup_gpio(pin, start)
        self.duty = -1
        self.set_angle(self.angle)
    
    # Set the GPIO Board as the current mode.
    def set_gpio_mode(self):
        GPIO.setmode(GPIO.BOARD)

    # Setup the GPIO for the specific pin.
    def setup_gpio(self, pin, start):
        GPIO.setup(pin, GPIO.OUT)
        pwm=GPIO.PWM(pin, self.hz)
        pwm.start(start)
        
        return pwm

    def calc_duty(self, angle):
        # int(angle / 18 + 2)
        r = myround(adjust(angle / 18 + 2))

        return r

    # For working with a single servo.
    # Need this to return a value just so we can preset the class 'duty' value.
    def set_angle(self, angle):
        duty = self.calc_duty(angle)

        # Don't send if nothing's changed.
        if self.duty == duty: return

        GPIO.output(self.pin,True)
        
        print("Duty {}".format(duty))

        self.pwm.ChangeDutyCycle((duty))
        sleep(1)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)
        
        self.duty = duty        

    # For cleanup of servo motor controls.
    def destroy_motor(self):
        self.pwm.stop()
        
