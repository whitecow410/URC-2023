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
servoM_b = Servomotor("P13")
servoM_c = Servomotor("P14")

fast = 140
slow = 50

m1.power(fast)
m2.power(fast)

threshold = []

times = 0
x = y = 0
a = b = 0


class event:
    move = None
    turn = None


class motor:
    def servoMA(angle=90):
        servoM_a.set_angle(angle)

    def servoMB(angleb=60, anglec=110):
        servoM_b.set_angle(angleb)
        servoM_c.set_angle(anglec)

    def set_speed(speed):
        m1.power(speed)
        m2.power(speed)


def detect(color=""):
    if color.lower() == "black":
        return True if ir.get_value() < threshold[0] and ir2.get_value() < threshold[1] else False
    elif color.lower() == "white":
        return True if ir.get_value() > threshold[0] and ir2.get_value() > threshold[1] else False
    else:
        return "white" if ir.get_value() > threshold[0] and ir2.get_value() > threshold[1] else "black"


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

    def left(auto=False):
        event.turn = lambda: move.left()
        if not auto:
            m1.cw()
            m2.ccw()
        else:
            move.left()
            while ir.get_value() > threshold[0]:
                pass
            move.stop()

    def right(auto=False):
        event.turn = lambda: move.right()
        if not auto:
            m1.ccw()
            m2.cw()
        else:
            move.right()
            while ir2.get_value() > threshold[1]:
                pass
            move.stop()


def pick(a=100, b=100, c=80):
    motor.servoMA(80)
    motor.servoMB(b, c)
    time.sleep(1)
    motor.servoMA(a)


def drop():
    motor.servoMA(118) if y == 1 else None
    time.sleep(0.5) if y == 1 else None
    motor.servoMB() if y == 0 else motor.servoMB(85, 80)
    motor.servoMA() if y != 1 else None


def fix():
    # motor.set_speed(slow)
    while ir.get_value() < threshold[0] or ir2.get_value() < threshold[1]:
        if ir.get_value() < threshold[0] and ir2.get_value() > threshold[1]:
            move.left()
        elif ir.get_value() > threshold[0] and ir2.get_value() < threshold[1]:
            move.right()
        else:
            break
    # smotor.set_speed(fast)


def setup():
    global threshold, t
    motor.servoMA()
    motor.servoMB()
    m1.brake()
    m2.brake()

    data = []
    for i in range(2):
        while button_a.is_pressed():
            pass
        display.show("W" if i == 0 else "B", delay=0)
        while not button_a.is_pressed():
            pass
        value = [ir.get_value(), ir2.get_value()]
        print(value)
        data += value
    threshold.append(
        int((data[0] + data[2]) / 2)
    )
    threshold.append(
        int((data[1] + data[3]) / 2)
    )
    print(threshold)
    while button_a.is_pressed():
        pass
    display.show("G", delay=0)
    while not button_a.is_pressed():
        pass
    display.clear()


def tracking():
    global times, x, y, a
    if times < 2:
        times += 1
    elif times >= 2:
        if x == 0:
            move.stop()
            pick()
            move.backward()
            while detect('black'):
                pass
            time.sleep(0.1)
            move.right(auto=True)
            fix()
            move.forward()
            times = 1
            x += 1
        elif x == 1:
            while detect('black'):
                pass
            time.sleep(0.3)
            move.right(auto=True) if y == 0 else move.left(auto=True)
            fix()
            a += 1
            if a == 2:
                x += 1
        elif x == 2:
            move.backward()
            time.sleep(1)
            move.forward()
            x += 1
        elif x == 3:
            move.stop()
            time.sleep(0.5)
            drop()
            move.backward()
            motor.servoMA(100)
            x += 1
        elif x == 4:
            move.forward()
            while detect('black'):
                pass
            time.sleep(0.1)
            move.left(auto=True)
            fix()
            event.move()
            x += 1
        elif x == 5:
            while detect('black'):
                pass
            time.sleep(0.1)
            move.right(auto=True)
            fix()
            times = 1
            x += 1
        elif x == 6:
            move.stop()
            pick(145)
            move.backward()
            while detect('black'):
                pass
            move.right(auto=True)
            fix()
            move.forward()
            x, y = 2, 1
    fix()
    event.move()
    while detect('black'):
        pass


# if __name__ == "__main__":
setup()
move.forward()
while True:
    if detect('black'):
        display.show("B", delay=0)
        tracking()
        display.clear()
    else:
        fix()
        event.move()
