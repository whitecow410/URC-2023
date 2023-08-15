from pyatcrobo2.parts import Servomotor, IRPhotoReflector, DCMotor
from pystubit.board import button_a, display, Image
import time
import math

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

tracking = False
picked = False


class location:
    map_ = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    robot = [2, 2, 0]

    cargo = [[0, 2], [0, 0], [0, 1]]

    point = [1, 1]


class event:
    move = None


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
        event.move = lambda: move.forward()
        m1.cw()
        m2.cw()

    def backward():
        event.move = lambda: move.backward()
        m1.ccw()
        m2.ccw()


class turn:
    global event

    def left(auto=False):
        if not auto:
            m1.cw()
            m2.ccw()
        else:
            move.left()
            time.sleep(1)
            while ir.get_value() > threshold[0]:
                move.left()

    def right(auto=False):
        if not auto:
            m1.ccw()
            m2.cw()
        else:
            move.right()
            time.sleep(1)
            while ir2.get_value() > threshold[1]:
                move.right()

    def position(position):
        global location
        if location.robot[2] == position:
            return
        diff = position - location.robot[2]

        if abs(diff) > 2 and diff > 0:
            diff -= 4
        elif abs(diff) > 2 and diff < 0:
            diff += 4

        def turn(): return turn.left if diff > 0 else turn.right
        for i in range(abs(diff)):
            turn()()
            while (ir2.get_value() > threshold[1]) if turn() == turn.left else (ir.get_value() > threshold[0]):
                pass
            while (ir.get_value() < threshold[0]) if turn() == turn.left else (ir2.get_value() < threshold[1]):
                pass
        move.stop()
        location.robot[2] = position


def detect(color):
    if color.lower() == "black":
        return True if ir.get_value() < threshold[0] and ir2.get_value() < threshold[1] else False
    elif color.lower() == "white":
        return True if ir.get_value() > threshold[0] and ir2.get_value() > threshold[1] else False


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
    global threshold
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


# if __name__ == "__main__":
setup()
if 1 not in location.map_[0] + location.map_[1] + location.map_[2]:
    move.forward()
    while detect("white"):
        pass
    move.stop()
    location.map_[location.robot[0]][location.robot[1]] = 1
while True:
    if not tracking:
        for i in location.cargo:
            if location.robot[1] == i[1]:
                for i in location.map_:
                    i[location.robot[1]] = 1
                tracking = True
                break
            elif location.robot[0] == i[0]:
                for i in location.map_:
                    i[location.robot[0]] = 1
                tracking = True
                break
            else:
                pass
    if tracking and not picked:
        location.mpa_[location.robot[0]][location.robot[1]] = 0
        while 1 in location.map_[0] + location.map_[1] + location.map_[2]:
            if location.robot[0] > 0:
                if location.map_[location.robot[0]-1][location.robot[1]] == 1:
                    
                elif location.robot[0] < 2 and location.map_[location.robot[0]+1][location.robot[1]] == 1:


                if location.robot[2] != 0:
                    turn.position(0)
                move.forward()
                while detect("back"):
                    fix()
                    move.forward()
                while detect("white"):
                    fix()
                    move.forward()
                location.robot[0] += 1
                location.mpa_[location.robot[0]][location.robot[1]] = 0

        move.stop()
