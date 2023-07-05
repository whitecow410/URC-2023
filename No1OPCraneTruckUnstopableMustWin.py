from pyatcrobo2.parts import Servomotor, IRPhotoReflector, DCMotor
from pystubit.board import button_a, display, Image
import time

ir = IRPhotoReflector("P1")
ir2 = IRPhotoReflector('P0')

m1 = DCMotor("M1")
m2 = DCMotor("M2")
m1.brake()
m2.brake()

servoM_a = Servomotor("P15")
servoM_b = Servomotor("P14")
servoM_c = Servomotor("P13")

fast = 100
slow = 50

m1.power(fast)
m2.power(fast)

threshold = []

times = 0
t = 0
x = y = 0
event = None
fix = False

class event:
    move = None
    turn = None

class motor:
    def servoMA(angle = 90):
        servoM_a.set_angle(angle)

    def servoMB(angleb = 30, anglec = 150):
        servoM_b.set_angle(angleb)
        servoM_c.set_angle(anglec)

    def set_speed(speed):
        m1.power(speed)
        m2.power(speed)

class move:
    def stop():
        m1.brake()
        m2.brake()

    def forward():
        global event
        display.show("F", delay = 0)
        m1.cw()
        m2.cw()
        event.move = lambda: move.forward

    class backward():
        global event
        def __init__(self):
            display.show("B", delay = 0)
            m1.ccw()
            m2.ccw()
            event.move = lambda: move.backward

        def fix():
            move.forward()
            time.sleep(0.3)
            motor.set_speed(slow)
            move.right(0.3) if event.turn() is move.left else move.left(0.3)
            motor.set_speed(fast)
            move.backward()

    def left(sleep=0):
        display.show("L", delay = 0)
        m1.cw()
        m2.ccw()
        time.sleep(sleep)

    def right(sleep=0):
        display.show("R", delay = 0)
        m1.ccw()
        m2.cw()
        time.sleep(sleep)

def pick():
    motor.servoMB(0, 180)
    time.sleep(1)
    motor.servoMA(130)

def drop():
    if y != 2:
        for i in range(130, 105, -18):
            motor.servoMA(i)
            time.sleep(0.5)
    motor.servoMB()

def setup():
    global threshold, t
    motor.servoMA()
    motor.servoMB()
    m1.brake()
    m2.brake()

    data = []
    s = 0
    for i in range(2):
        while button_a.is_pressed():
            pass
        display.show("W" if i == 0 else "B", delay = 0)
        while not button_a.is_pressed():
            pass
        s = 2
        value = [ir.get_value(), ir2.get_value()]
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
    display.show("T", delay = 0)
    while not button_a.is_pressed():
        pass
    while button_a.is_pressed():
        pass
    move.left()
    while not button_a.is_pressed():
        s += 1
        time.sleep(0.1)
    move.stop()
    t = s/10
    print(t)
    while button_a.is_pressed():
        pass
    display.show("G", delay = 0)
    while not button_a.is_pressed():
        pass

def square():
    global times, x, y
    if times >= 0 and times < 2:
        event.move()()
        times += 1
        time.sleep(0.5)
    elif times >= 2:
        if x == 0:
            move.backward()
            time.sleep(0.5)
            move.stop()
            pick()
            move.backward()
            times = 1
            x += 1
            time.sleep(0.5)
        elif x == 1:
            move.forward()
            time.sleep(1)
            move.left(t)
            x += 1 if y != 1 else 3
            time.sleep(0.5)
        elif x == 2:
            event.move()()
            time.sleep(1)
            move.right(t)
            x += 1
            time.sleep(0.5)
        elif x == 3:
            drop()
            move.backward()
            time.sleep(1)
            y = x = 1
        elif x == 4:
            motor.servoMB()
            move.forward()
            x += 1
        elif x == 5:
            motor.servoMB(0, 180)
            time.sleep(0.5)
            motor.servoMB()
            move.backward()
            time.sleep(1)
            move.stop()
            pick()
            move.backward()
            y = x = 2



    # elif times >= 2:
    #     move.forward()
    #     time.sleep(0.5)``
    #     move.left(l)
    #     times = 1

def tracking():
    global event, fix
    if ir.get_value() < threshold[0] and ir2.get_value() < threshold[1]:
        image = Image('00000:01100:01010:00110:00000')
        image.set_base_color((0, 31, 31))
        display.show(image, delay = 0)
        move.stop()
        time.sleep(0.5)
        square()
    elif ir.get_value() < threshold[0] and ir2.get_value() > threshold[1]:
        motor.set_speed(slow)
        move.left()
        motor.set_speed(fast)
        event.turn = lambda: move.left
        # fix = True if event.move() is move.backward else False
    elif ir.get_value() > threshold[0] and ir2.get_value() < threshold[1]:
        motor.set_speed(slow)
        move.right()
        motor.set_speed(fast)
        event.turn = lambda: move.right
        # fix = True if event.move() is move.backward else False
    else:
        # if fix:
        #     move.backward.fix()
        #     fix = False
        event.move()()

# if __name__ == "__main__":
setup()
move.forward()
while True:
    tracking()