import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


# Base class for a stepper motor controller
class PulleyMotor(object):

    # Define GPIO signals to use
    direction_pin = 7  # Pin 26, GPIO7
    step_pin = 8  # Pin 24, GPIO8
    backwards = False
    step_frequency = .0005

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        self.setup_pins()

    # Set all pins as output
    def setup_pins(self):
        for pin in [step_pin, direction_pin]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def step(self):
        GPIO.output(self.step_pin, True)
        time.sleep(self.step_frequency)
        GPIO.output(self.step_pin, False)
        time.sleep(self.step_frequency)

    def set_reverse(self, reverse=False):
        GPIO.output(self.direction_pin, reverse)

    def move(self, result_queue=None, distance=0, clockwise=True, name='first'):
        steps = 0
        print "%s %s %s" % (name, distance < 0, self.backwards)
        if distance < 0:
            self.set_reverse(True != self.backwards)
            steps = int(-distance)
        else:
            self.set_reverse(False != self.backwards)
            steps = int(distance)  # some multiplier
        for i in range(steps):
            self.step()
        if result_queue:
            try:
                result_queue.put(name)
            except:
                pass
