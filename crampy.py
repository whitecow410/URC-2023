from pyatcrobo2.parts import IRPhotoReflector, DCMotor, Servomotor
from pystubit.board import button_a, display
import time

ir = IRPhotoReflector("P0")
ir2 = IRPhotoReflector('P1')

m1 = DCMotor("M1")
m2 = DCMotor("M2")
fast = 100
slow = 50

m1.power(fast)
m2.power(fast)
m1.brake()
m2.brake()
a = 0
b = 0

T = 1

x = 0
y = 0

sag = [60, 70, 80, 90, 110]
sbg = [120, 110, 100, 90, 70]

lefthold = [60, 70, 80, 90]
righthold = [120, 110, 100, 90]

display.clear()

servoM_a = Servomotor("P13")
#greater num inner angle
servoM_c = Servomotor("P16")
#greater num upper
servoM_b = Servomotor("P14")
#greater num outter angle
threshold = 0
threshold2 = 0

def line():
    global threshold, threshold2
    print("white")
    display.show("W", delay = 0)

    while not button_a.is_pressed():
        pass
    white1 = ir.get_value()
    white2 = ir2.get_value()
    print(white1, white2)
    print("black")
    display.show("B", delay = 0)
    time.sleep(5)
    black1 = ir.get_value()
    black2 = ir2.get_value()
    print(black1, black2)
    display.clear()
    time.sleep(4)


    threshold = int((white1 + black1) /2)
    threshold2 = int((white2 + black2) /2)

def standby():
    servoM_a.set_angle(60)
    servoM_b.set_angle(120)
    time.sleep(0.5)
    servoM_c.set_angle(75)

def grab():
    servoM_c.set_angle(75)
    for i, a in zip(sag, sbg):
        servoM_a.set_angle(i)
        servoM_b.set_angle(a)
        time.sleep(0.2)
    time.sleep(1)
    servoM_c.set_angle(140)
    time.sleep(0.5)

def place():
    for i in range(140, 60, -5):
        time.sleep(0.2)
        servoM_c.set_angle(i)
    servoM_a.set_angle(90)
    servoM_b.set_angle(90)
    servoM_c.set_angle(75)

def placeB():
    m1.ccw()
    m2.ccw()
    time.sleep(0.5)
    m1.brake()
    m2.brake()
    for i in range(140, 100, -5):
        time.sleep(0.2)
        servoM_c.set_angle(i)
    servoM_a.set_angle(90)
    servoM_b.set_angle(90)
    servoM_c.set_angle(110)


def release():
    for i, a in zip(sag, sbg):
        servoM_a.set_angle(a)
        servoM_b.set_angle(i)
        time.sleep(0.2)


def backward():
    m1.power(fast)
    m2.power(fast)
    display.show("F", delay = 0)
    m1.ccw()
    m2.ccw()
    time.sleep(a)
    m1.brake()
    m2.brake()

def forward():
    m1.power(fast)
    m2.power(fast)
    display.show("F", delay = 0)
    m1.cw()
    m2.cw()
    time.sleep(a)
    m1.brake()
    m2.brake()

def hold():
    for i, a in zip(sag, sbg):
        servoM_a.set_angle(i)
        servoM_b.set_angle(a)
        time.sleep(0.2)


def square():
    global x
    if x == 0:
        hold()
        forward()
        x += 1
    elif x == 1:
        forward()
        x += 1
    elif x == 2:
        forward()
        left()
        x = 1

def test():
    global x, T
    if x == 0:
        hold()
        reset()
        forward()
        left()
        stop()
        x += 1
    elif x == 1:
        forward()
        right()
        stop()
        release()
        reset()
        T = 2
        x = 0

def reset():
    global y
    backward()
    while not y == 1:
        parking()
    m1.power(fast)
    m2.power(fast)
    y = 0


def track1():
    display.show("1", delay = 0)
    global x, T
    if x == 0:
        grab()
        forward()
        left()
        x += 1
    elif x == 1:
        forward()
        right()
        x += 1
    elif x == 2:
        place()
        time.sleep(1)
        reset()
        T = 2
        x = 0

def track2():
    global x, T
    display.show("2", delay = 0)
    if x == 0:
        servoM_c.set_angle(140)
        forward()
        left()
        stop()
        servoM_a.set_angle(75)
        servoM_b.set_angle(110)
        servoM_c.set_angle(75)
        time.sleep(1)
        x += 1
    elif x == 1:
        grab()
        reset()
        forward()
        right()
        forward()
        x += 1
    elif x == 2:
        placeB()
        reset()
        T = 0
        x = 0


def check():
    global a, b
    display.show("O", delay = 0)
    while not button_a.is_pressed():
        pass
    display.show("1", delay = 0)
    time.sleep(1)
    run()
    while not button_a.is_pressed():
        a += 1
        time.sleep(0.1)
        pass
    stop()
    display.show("2", delay = 0)
    m2.power(50)
    m1.cw()
    m2.ccw()
    while not button_a.is_pressed():
        time.sleep(0.1)
        b += 1
    a = a/10
    b = b/10
    print(a, b)
    run()
    stop()


def tracking():
    m1.power(fast)
    m2.power(fast)
    if ir.get_value() < threshold and ir2.get_value() < threshold2:
        display.show("B", delay = 0)
        m1.brake()
        m2.brake()
        time.sleep(1)
        if T == 1:
            square()
        elif T == 2:
            track2()
        else:
            display.show("E", delay = 0)
            time.sleep(30)
    elif ir.get_value() < threshold and ir2.get_value() > threshold2:
        m1.ccw()
        m2.cw()
    elif ir2.get_value() < threshold2 and ir.get_value() > threshold:
        m1.cw()
        m2.ccw()
    else:
        m1.cw()
        m2.cw()
        display.clear()

def parking():
    global y
    if ir.get_value() < threshold and ir2.get_value() < threshold2:
        display.show("B", delay = 0)
        m1.brake()
        m2.brake()
        y += 1
    elif ir.get_value() < threshold and ir2.get_value() > threshold2:
        m1.cw()
        m2.ccw()
    elif ir2.get_value() < threshold2 and ir.get_value() > threshold:
        m1.ccw()
        m2.cw()
    else:
        m1.ccw()
        m2.ccw()
        display.clear()

def stop():
    m1.brake()
    m2.brake()
    time.sleep(1)

def run():
    m1.power(fast)
    m2.power(fast)
    m1.cw()
    m2.cw()

def left():
    print(b)
    m1.power(fast)
    m2.power(slow)
    m1.cw()
    m2.ccw()
    time.sleep(b)

def right():
    print(b)
    m1.power(slow)
    m2.power(fast)
    m1.ccw()
    m2.cw()
    time.sleep(b)

standby()
check()
line()
while True:
    tracking()