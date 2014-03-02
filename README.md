Stipplebot
==========

This library was written to control a stippling art project. 

# Hardware 

- Raspberry Pi running Raspbian or some other operating system that provides the RPi.GPIO Python module
- Two stepper motor driver boards, like the [Big Easy Driver](https://www.sparkfun.com/products/11876)
- Two bipolar stepper motors, like [these](https://www.sparkfun.com/products/10846) with 68 oz-in torque and 400 steps/rev
- 12-volt power supply for the stepper motors
- One small servo motor for the pen head, like [this](https://www.sparkfun.com/products/10333) with metal gears and 40 oz-in torque

# Getting Started

- Run the servo daemon available at servod/servod
- Initialize a stippler manager, add points, and start drawing

    stippler = StippleManager(x=12000, y=12000, width=38000)
    stippler.points_to_draw = [(16000, 20000), (8000, 10000), (12000, 12000)]
    stippler.start_drawing()

Good luck!