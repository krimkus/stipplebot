#!/usr/bin/env python
"""
Deprecated since the solenoid was not strong enough.

Was using: https://www.sparkfun.com/products/11015
5v, 4.5mm throw
"""

# Import required libraries
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Base class for a solenoid motor controller using a stepper ULN2003 controller
class SolenoidMotor(object):

    # # Define GPIO signals to use
    # Pin 13, GPIO27
    pin = 27
    wait_time = .01
    wait_time = .1

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        # Set pin as output
        print "Setup pin"
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)

    def tap(self):
        GPIO.output(self.pin, True)
        time.sleep(self.wait_time)
        GPIO.output(self.pin, False)

    def reset(self):
        GPIO.output(self.pin, False)


if __name__ == "__main__":
    pen = SolenoidMotor()
    start_time = time.time()
    for i in range(8):
        pen.tap()
        time.sleep(.09)
    print time.time() - start_time
    pen.reset()
