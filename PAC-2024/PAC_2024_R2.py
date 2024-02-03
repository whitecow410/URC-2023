from pyatcrobo2.parts import DCMotor, IRPhotoReflector
from pystubit.board import button_a, button_b, display, Image
import time

m1 = DCMotor("M1")
m2 = DCMotor("M2")
m1.brake()
m2.brake()

ir = IRPhotoReflector('P0')

threshold = 2780
x = 0

class setSpeed:
    def forward():
        return 100, 100

    def backward():
        return 100, 100

    def set_speed(m01, m02):
        m1.power(m01)
        m2.power(m02)


class move:
    def stop():
        m1.brake()
        m2.brake()
        display.clear()

    def forward():
        m1.cw()
        m2.cw()
        display.show(Image('00100:01110:00000:00100:00100'))

    def backward():
        m1.ccw()
        m2.ccw()
        display.show(Image('00100:00100:00000:01110:00100'))

    def left():
        m1.ccw()
        m2.cw()
        display.show(Image('00000:01100:01000:00010:00000'))

    def right():
        m1.cw()
        m2.ccw()
        display.show(Image('00000:00110:00010:01000:00000'))


def setup():
    global threshold
    move.stop()

    # get threhold
    if not threshold:
        value = []
        for i in range(2):
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
    setSpeed.set_speed(145, 150)
    display.show("G", delay=0)
    while not button_b.is_pressed():
        pass
    display.clear()

def tracking():
    global x
    if x > 0:
        if x <= 2:
            move.stop()
            move.backward()
            time.sleep(0.55)
            move.left()
            time.sleep(0.2)
            move.forward()
        elif x == 3:
            move.stop()
            move.backward()
            time.sleep(0.55)
            move.right()
            time.sleep(0.2)
            move.forward()
        elif x == 4:
            move.stop()
            move.backward()
            time.sleep(0.55)
            move.right()
            time.sleep(0.135)
            move.forward()
        elif x == 5:
            move.stop()
            for x in range(5):
                for y in range(5):
                    display.set_pixel(x, y, (31, 31, 31))
        
    while ir.get_value() < threshold:
        pass
    x += 1


setup()
move.forward()
while True:
    while ir.get_value() < threshold:
        tracking()
