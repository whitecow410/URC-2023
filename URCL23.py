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


class move:
    global event

    def stop():
        m1.brake()
        m2.brake()

    def forward():
        event.move = lambda: move.forward
        m1.cw()
        m2.cw()

    def backward():
        event.move = lambda: move.backward
        m1.ccw()
        m2.ccw()

    def left(auto=False):
        event.turn = lambda: move.left
        if not auto:
            m1.cw()
            m2.ccw()
        else:
            move.left()
            time.sleep(1)
            while ir.get_value() > threshold[0]:
                move.left()

    def right(auto=False):
        event.turn = lambda: move.right
        if not auto:
            m1.ccw()
            m2.cw()
        else:
            move.right()
            time.sleep(1)
            while ir2.get_value() > threshold[1]:
                move.right()


def pick(a=90, b=100, c=80):
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


def square():
    global times, x, y
    if times >= 0 and times < 2:
        event.move()()
        times += 1
        time.sleep(0.5)
    elif times >= 2:
        if x == 0:
            move.stop()
            motor.servoMA(80)
            pick(100)
            motor.servoMA(100)
            motor.set_speed(200)
            while ir.get_value() < threshold[0] and ir2.get_value() < threshold[1]:
                event.move()()
            move.stop()
            motor.set_speed(fast)
            move.right(auto=True)
            move.stop()
            fix()
            motor.servoMA(90)
            move.forward()
            times = x = 1
        elif x == 1:
            time.sleep(1)
            while ir.get_value() < threshold[0] and ir2.get_value() < threshold[1]:
                event.move()()
            move.right(auto=True)
            move.stop()
            fix()
            event.move()()
            time.sleep(0.5)
            x += 1
        elif x == 2:
            time.sleep(1)
            while ir.get_value() < threshold[0] and ir2.get_value() < threshold[1]:
                event.move()()
            move.right(auto=True) if y == 0 else move.left(auto=True)
            move.stop()
            fix()
            event.move()()
            time.sleep(0.5)
            x += 1
        elif x == 3:
            move.backward() if y == 1 else None
            time.sleep(0.3) if y == 1 else None
            move.stop()
            time.sleep(0.5)
            drop()
            move.backward()
            time.sleep(0.5)
            x += 1 if y == 0 else 3
        elif x == 4:
            move.forward()
            time.sleep(1)
            while ir.get_value() < threshold[0] and ir2.get_value() < threshold[1]:
                event.move()()
            move.left(auto=True)
            move.stop()
            fix()
            motor.servoMB(angleb=70, anglec=130)
            motor.servoMA(80)
            move.forward()
            time.sleep(0.5)
            x += 1
        elif x == 5:
            move.stop()
            pick(145, 105, 75)
            move.backward()
            time.sleep(0.5)
            while ir.get_value() < threshold[0] and ir2.get_value() < threshold[1]:
                event.move()()
            move.left(auto=True)
            move.stop()
            fix()
            move.forward()
            x, y = 2, 1
        elif x == 6:
            while True:
                move.stop()

    # elif times >= 2:
    #     move.forward()
    #     time.sleep(0.5)
    #     move.left(l)
    #     times = 1


def tracking():
    global event, fix
    if ir.get_value() < threshold[0] and ir2.get_value() < threshold[1]:
        square()
    else:
        fix()
        event.move()()


# if __name__ == "__main__":
setup()
move.forward()
while True:
    tracking()
