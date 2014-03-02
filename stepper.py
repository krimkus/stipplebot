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


# Base class for a stepper motor controller
class PenMotor(object):

    # # Define GPIO signals to use
    # # Pins 18,22,24,26
    # # GPIO24,GPIO25,GPIO8,GPIO7
    # pins = [24, 25, 8, 7]

    # Pins 13,15,21,23
    # GPIO27,GPIO22,GPIO9,GPI11
    pins = [27, 22, 9, 11]

    wait_time = 0
    sequence = []

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        self.setup_pins()
        if getattr(kwargs, 'use_short_sequence', False):
            print "using short"
            self.sequence.append([1, 0, 0, 0])
            self.sequence.append([0, 1, 0, 0])
            self.sequence.append([0, 0, 1, 0])
            self.sequence.append([0, 0, 0, 1])
            self.wait_time = .002
        else:
            print "using long"
            self.sequence.append([1, 0, 0, 0])
            self.sequence.append([1, 1, 0, 0])
            self.sequence.append([0, 1, 0, 0])
            self.sequence.append([0, 1, 1, 0])
            self.sequence.append([0, 0, 1, 0])
            self.sequence.append([0, 0, 1, 1])
            self.sequence.append([0, 0, 0, 1])
            self.sequence.append([1, 0, 0, 1])
            self.wait_time = .001

    # Set all pins as output
    def setup_pins(self):
        for pin in self.pins:
            print "Setup pins"
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def step(self, reverse=False):
        for sequence_pulse in reversed(self.sequence) if reverse else self.sequence:
            #print " current sequence_pulse: %s" % sequence_pulse
            for pin in range(0, 4):
                if sequence_pulse[pin] == 1:
                    #print " Pulsing pin %i" % (self.pins[pin])
                    GPIO.output(self.pins[pin], True)
                else:
                    GPIO.output(self.pins[pin], False)
            time.sleep(self.wait_time)

    def tap(self):
        steps = 6
        for i in range(steps):
            pen.step()
        for i in range(steps):
            pen.step(reverse=True)
        if hasattr(self, 'parent') and hasattr(self.parent, 'tap_finished'):
            self.parent.tap_finished()

    def adjust(self, steps=0, reverse=False):
        for i in range(steps):
            pen.step(reverse=reverse)


if __name__ == "__main__":
    pen = PenMotor()
    start_time = time.time()
    for i in range(10):
        pen.tap()
        time.sleep(.1)
    print time.time() - start_time
