from pyatcrobo2.parts import Servomotor, IRPhotoReflector, DCMotor
from pystubit.board import button_a, display
import time

ir = IRPhotoReflector("P1")
ir2 = IRPhotoReflector('P0')
ir3 = IRPhotoReflector('P2')

m1 = DCMotor("M1")
m2 = DCMotor("M2")
m1.brake()
m2.brake()

servoM_a = Servomotor("P15")
servoM_b = Servomotor("P13")
servoM_c = Servomotor("P14")

fast = 120
slow = 50

m1.power(fast)
m2.power(fast)

threshold = []  # 2000, 2400

times = 0
x = y = z = 0
a = b = 0


class event:
    move = None
    turn = None


class motor:
    def servoMA(angle=90):
        servoM_a.set_angle(angle)

    def servoMB(angleb=55, anglec=115):
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
            move.stop()

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
            move.stop()


def pick(a=110, b=98, c=82):  # 55 115
    motor.servoMA(80)
    time.sleep(0.3)
    motor.servoMB(b, c)
    time.sleep(1)
    motor.servoMA(a)


def drop(a=None):
    if a:
        motor.servoMA(a)
        time.sleep(0.3)
    motor.servoMB()
    motor.servoMA()


def fix():
    # motor.set_speed(slow)
    while (ir.get_value() < threshold[0] or ir2.get_value() < threshold[1]) and event.move != move.backward:
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
    if not threshold:
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
    global times, x, y, z, a
    if times < 1:
        times += 1
    else:
        if x == 0:
            time.sleep(0.1)
            motor.servoMA(145)
            move.backward()
            time.sleep(1)
            move.left(auto=True)
            fix()
            move.backward()
            time.sleep(0.5)
            move.forward()
            x += 1
        elif x == 1:
            time.sleep(2.5)
            move.left()
            time.sleep(1.3)
            move.forward()
            time.sleep(0.5)
            while detect('white'):
                pass
            time.sleep(0.5)
            move.left(auto=True)
            motor.set_speed(fast)
            fix()
            x += 1
        elif x == 2:
            move.backward()
            while ir3.get_value() > 1800:
                pass
            move.stop()
            pick()
            time.sleep(0.3)
            move.forward()
            while detect('white'):
                pass
            time.sleep(0.35)
            fix()
            move.left(auto=True)
            fix()
            move.forward()
            x += 1
        elif x == 3:
            while detect('black'):
                pass
            time.sleep(0.35)
            fix()
            move.right(auto=True)
            fix()
            move.forward()
            x += 1
        elif x == 4:
            move.stop()
            move.backward()
            while detect('black'):
                pass
            time.sleep(0.15)
            move.stop()
            drop(98)
            move.backward()
            x += 1
        elif x == 5:
            move.forward()
            while detect('black'):
                pass
            time.sleep(0.35)
            fix()
            if z < 1:
                move.right(auto=True) if y < 1 else move.left(auto=True)
            else:
                move.left(auto=True) if y < 1 else move.right(auto=True)
            y += 1
            if y >= 2:
                y = 0
                x += 1
        elif x == 6:
            while ir3.get_value() < 2850:
                pass
            move.stop()
            pick(160) if z == 0 else pick(145)
            move.right(auto=True) if z == 0 else move.left(auto=True)
            move.forward()
            x += 1
            times = 0
        elif x == 7:
            time.sleep(2.5)
            move.right() if z == 0 else move.left()
            time.sleep(1.5)
            move.forward()
            time.sleep(0.5)
            while detect('white'):
                pass
            time.sleep(0.5)
            move.right(auto=True) if z == 0 else move.left(auto=True)
            motor.set_speed(fast)
            fix()
            x += 1
        elif x == 8:
            l = 145
            if z == 0:
                time.sleep(0.35)
                move.stop()
                while l > 80:
                    l -= 5
                    motor.servoMA(l)
                    time.sleep(0.3)
                move.stop()
                motor.servoMB(88, 92)
                motor.servoMA(90)
                move.forward()
                time.sleep(1.8)
                move.stop()
                motor.servoMB()
            elif z > 0:
                while ir3.get_value() < 2850:
                    pass
                move.stop()
                time.sleep(0.3)
                sg = [100, 80]
                while l > 120:
                    l -= 5
                    motor.servoMA(l)
                    time.sleep(0.3)
                while sg[0] > 85 and sg[1] < 95:
                    sg[0] -= 2
                    sg[1] += 2
                    motor.servoMB(sg[0], sg[1])
                    time.sleep(0.3)
                time.sleep(0.2)
                motor.servoMB()
            motor.servoMA(145)
            move.backward()
            if z <= 0:
                z += 1
                x = 5
            else:
                x += 1
        elif x == 9:
            move.stop()
            motor.servoMA(90)
            for i in range(12):
                motor.servoMB(100, 80)
                time.sleep(0.3)
                motor.servoMB()
                time.sleep(0.3)
            time.sleep(1000)

    fix()
    event.move()()
    while detect('black'):
        pass


# if __name__ == "__main__":
setup()
move.forward()
while True:
    if detect('black'):
        tracking()
    else:
        fix()
        event.move()()
