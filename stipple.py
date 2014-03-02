#!/usr/bin/env python
import math
import multiprocessing
import threading

from bigeasy import PulleyMotor
from servo import ServoMotor


def hypotenuse(adj, opp):
    return math.sqrt(adj*adj+opp*opp)


class StippleManager(object):
    """
    Current hardware configuration:
    For x and y coordinates, 500 = 1/4 inch
    For width, 38000 = 19"
    """

    def __init__(self, x=0, y=0, width=200):
        self.left_pulley_moving = False
        self.right_pulley_moving = False
        self.x = x
        self.y = y
        self.width = width

        self.left_pulley_position = hypotenuse(x, y)
        self.right_pulley_position = hypotenuse(width-x, y)

        self.left_pulley = PulleyMotor(parent=self, direction_pin=7, step_pin=8, backwards=True)
        self.right_pulley = PulleyMotor(parent=self, direction_pin=24, step_pin=23)
        self.pen = ServoMotor()

        self.pulley_queue = multiprocessing.Queue()

        self.points_to_draw = []

    def add_points(self, points):
        self.points_to_draw += points

    def get_coords(self):
        return "%s, %s" % (self.x, self.y)

    def start_drawing(self):
        drawing_thread = threading.Thread(target=self.draw)

    def stop_drawing(self):
        self._stop_drawing = True

    def draw(self):
        if self._stop_drawing:
            # We received a message to stop drawing, so stop drawing dots and reset the message
            self._stop_drawing = False
        else:
            # Pop a point off the front of our points array
            if self.points_to_draw:
                next_point = self.points_to_draw.pop(0)
                new_x = next_point[0]
                new_y = next_point[1]

                # Calculate pulley lengths for new coords
                new_left_pulley_position = hypotenuse(new_x, new_y)
                new_right_pulley_position = hypotenuse(self.width-new_x, new_y)

                # Figure out diff between old and new pulley lengths now so
                # that properties on self can be set before pulleys are moved
                diff_lpp = new_left_pulley_position - self.left_pulley_position
                diff_rpp = new_right_pulley_position - self.right_pulley_position

                print "Going to move %s %s" % (diff_lpp, diff_rpp)

                # Setting properties before actually moving pulleys
                self.left_pulley_position = new_left_pulley_position
                self.right_pulley_position = new_right_pulley_position
                self.x = new_x
                self.y = new_y

                if new_x > 0 and new_x < self.width and new_y > 0:
                    self.left_pulley_moving = True
                    self.right_pulley_moving = True

                    multiprocessing.Process(target=self.left_pulley.move, args=[self.pulley_queue, diff_lpp, True, 'first']).start()
                    multiprocessing.Process(target=self.right_pulley.move, args=[self.pulley_queue, diff_rpp, True, 'second']).start()

                    print "Waiting for result..."

                    result = self.pulley_queue.get()  # waits until any of the proccess have `.put()` a result
                    result2 = self.pulley_queue.get()

                    print result
                    print result2

                    self.pen.tap()

                # Draw next point
                self.draw()


if __name__ == "__main__":

    stippler = StippleManager(x=12000, y=12000, width=38000)
    stippler.pen.goto(0)
    #stippler.points_to_draw = [(16000, 20000), (8000, 10000), (12000, 12000)]
    stippler.add_points([(12000 + (x - (x % 2)) * 100, 12000 + ((x % 2) * 400)) for x in range(10)])
    stippler.start_drawing()
    stippler.stop_drawing()
    stippler.get_coords()
