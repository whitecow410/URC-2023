from pyatcrobo2.parts import Servomotor, IRPhotoReflector, DCMotor
from pystubit.board import display, button_a
import time

m1 = DCMotor("M1")
m2 = DCMotor("M2")
m1.brake()
m2.brake()

ir = IRPhotoReflector('P0')
servoM= Servomotor("P13")

fast = 100
slow = 50

m1.power(fast)
m2.power(fast)

detect = 'thr'
threshold = None
color = None


class event:
    move = None
    turn = None


class motor:
    def set_speed(speed):
        m1.power(speed)
        m2.power(speed)


def detect(color=""):
    if color.lower() == "black":
        return True if ir.get_value() > threshold else False
    elif color.lower() == "white":
        return True if ir.get_value() < threhold else False
    else:
        return "white" if ir.get_value() < threshold else "black"


class move:
    global event

    def stop():
        m1.brake()
        m2.brake()

    def forward():
        event.move = lambda: move.forward()
        m1.cw()
        m2.cw()

    def backward():
        event.move = lambda: move.backward()
        m1.ccw()
        m2.ccw()

    def left():
        event.turn = lambda: move.left()
        m1.cw()
        m2.ccw()

    def right():
        event.turn = lambda: move.right()
        m1.ccw()
        m2.cw()


def setup():
    global threshold, color
    move.stop()

    # threhold
    if not threshold:
        value = []
        for i in range(1):
            while button_a.is_pressed():
                pass
            display.show("W" if i == 0 else "B", delay=0)
            while not button_a.is_pressed():
                pass
            value.append(ir.get_value())
        threshold = int((value[0] + value[1]) / 2)
        print(threshold)
        while button_a.is_pressed():
            pass
    
    # Run
    display.show("G", delay=0)
    while not button_a.is_pressed():
        pass
    display.clear()

def cross_line():
    move.forward()

    while ir.get_value() > threhold:
        pass
    while ir.get_value() < threhold:
        pass

def tracking():
    stop() if ir.get_value > threhold else move.forward()

# if __name__ == "__main__":
setup()
while True:
    tracking()
