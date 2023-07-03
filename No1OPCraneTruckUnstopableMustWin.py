from pyatcrobo2.parts import Servomotor, IRPhotoReflector, DCMotor
from pystubit.board import button_a, display, Image

import time

ir = IRPhotoReflector("P0")
ir2 = IRPhotoReflector('P1')

m1 = DCMotor("M1")
m2 = DCMotor("M2")
m1.brake()
m2.brake()

servoM_a = Servomotor("P16")
servoM_b = Servomotor("P15")

fast = 120
slow = 50

m1.power(fast)
m2.power(fast)

threshold = []

times = 0
l = r = 0

def servoMA(angle = 100):
    servoM_a.set_angle(angle)
    return angles

def servoMB(angle = 100):
    servoM_b.set_angle(angle)
    return angle

class move:
    def stop():
        m1.brake()
        m2.brake()

    def forward():
        display.show("F", delay = 0)
        m1.ccw()
        m2.ccw()

    def backward():
        display.show("B", delay = 0)
        m1.cw()
        m2.cw()

    def left(sleep=None):
        display.show("L", delay = 0)
        m1.cw()
        m2.ccw()
        time.sleep(sleep if sleep or sleep == 0 else l)

    def right(sleep=None):
        display.show("R", delay = 0)
        m1.ccw()
        m2.cw()
        time.sleep(sleep if sleep or sleep == 0 else r)

def grab():
    servoMA(angle=100)
    time.sleep(1.5)
    servoMA()
    time.sleep(1.5)
    servoMB(angle=140)

def drop():
    for i in range(140, 100, -10):
        servoM_a.set_angle(i)

def setup():
    global threshold, l, r
    servoMA()
    servoMB()
    m1.brake()
    m2.brake()

    data = []
    for i in range(2):
        display.show("W" if i == 0 else "B", delay = 0)
        while not button_a.is_pressed():
            pass
        s = 2
        while s > 0:
            value = [ir.get_value(), ir2.get_value()]
            s -= 1
            time.sleep(0.75)
        print(value)
        data += value
    threshold.append(
        int((data[0] + data[2]) /2)
    )
    threshold.append(
        int((data[1] + data[3]) /2)
    )
    print(threshold)
    while button_a.is_pressed():
        pass
    for i in range(2):
        if i == 0:
            display.show("L", delay = 0)
            turn = lambda: move.left()
        else:
            display.show("R", delay = 0)
            turn = lambda: move.right()
        while button_a.is_pressed():
            pass
        while not button_a.is_pressed():
            pass
        turn()
        while button_a.is_pressed():
            pass
        while not button_a.is_pressed():
            s += 1
            time.sleep(0.1)
        move.stop()
        if i == 0:
            l = s/10
        else:   
            r = s/10
    print(l, r)
    while button_a.is_pressed():
        pass
    display.show("G", delay = 0)
    while not button_a.is_pressed():
        pass

def square():
    global times
    if times >= 0 and times < 2:
        move.forward()
        time.sleep(0.5)
        times += 1
    elif times >= 2:
        move.forward()
        time.sleep(0.3)
        move.left()
        times = 1

def tracking():
    if ir.get_value() < threshold[0] and ir2.get_value() < threshold[1]:
        image = Image('00000:01100:01010:00110:00000')
        image.set_base_color((0, 31, 31))
        display.show(image, delay = 0)
        move.stop()
        time.sleep(0.5)
        square()
    elif ir.get_value() < threshold[0] and ir2.get_value() > threshold[1]:
        move.left(0)
    elif ir.get_value() > threshold[0] and ir2.get_value() < threshold[1]:
        move.right(0)
    else:
        move.forward()

setup()
while True:
    tracking()