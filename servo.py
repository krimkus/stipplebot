#!/usr/bin/env python
import time
import os


# Base class for a servo motor controller using ServoBlaster
class ServoMotor(object):

    # how long it takes to get the pen down before lifting back up
    wait_time = .9

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])

    def tap(self):
        os.system('echo 0=100 > /dev/servoblaster')
        time.sleep(self.wait_time)
        os.system('echo 0=142 > /dev/servoblaster')

    def goto(self, position):
        os.system('echo 0=%s > /dev/servoblaster' % position)


# To test tapping five times with .4 second pauses between each tap
if __name__ == "__main__":
    pen = ServoMotor()
    start_time = time.time()
    time_between_taps = .4
    for i in range(5):
        pen.tap()
        time.sleep(time_between_taps)
    print time.time() - start_time

    pen.goto(0)
