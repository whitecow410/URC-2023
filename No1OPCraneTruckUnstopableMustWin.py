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
x = y = 0

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
    global event
    def stop():
        m1.brake()
        m2.brake()

    def forward():
        display.show("F", delay = 0)
        event.move = lambda: move.forward
        m1.cw()
        m2.cw()

    def backward():
        display.show("B", delay = 0)
        event.move = lambda: move.backward
        m1.ccw()
        m2.ccw()

    def left(sleep=0):
        display.show("L", delay = 0)
        event.turn = lambda: move.left
        m1.cw()
        m2.ccw()
        time.sleep(sleep)

    def right(sleep=0):
        display.show("R", delay = 0)
        event.turn = lambda: move.right
        m1.ccw()
        m2.cw()
        time.sleep(sleep)

def pick():
    motor.servoMB(0, 180)
    time.sleep(1)
    motor.servoMA(130)

def drop():
    if y != 1:
        for i in range(130, 105, -18):
            motor.servoMA(i)
            time.sleep(0.5)
    motor.servoMB()

def fix():
    motor.set_speed(slow)
    while ir.get_value() < threshold[0] or ir2.get_value() < threshold[1]:
        if ir.get_value() < threshold[0] and ir2.get_value() > threshold[1]:
            move.left()
        elif ir.get_value() > threshold[0] and ir2.get_value() < threshold[1]:
            move.right()
        else:
            break
    motor.set_speed(fast)

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
        display.show("W" if i == 0 else "B", delay = 0)
        while not button_a.is_pressed():
            pass
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
            time.sleep(0.5)
            move.stop()
            pick()
            move.backward()
            time.sleep(0.5)
            while ir.get_value() > threshold[0]:
                move.left()
            move.stop()
            fix()
            move.forward()
            times = 1
            x += 1
            time.sleep(0.5)
        elif x == 1:
            move.forward()
            time.sleep(1)
            while ir2.get_value() > threshold[1]:
                move.right()
            move.stop()
            fix()
            event.move()()
            x += 1
            time.sleep(0.5)
        elif x == 2:
            event.move()()
            time.sleep(1)
            while ir2.get_value() > threshold[1]:
                move.right()
            move.stop()
            fix()
            event.move()()
            x += 1
            time.sleep(0.5)
        elif x == 3:
            move.backward()
            time.sleep(1)
            move.stop()
            drop()
            move.backward()
            x += 1 if y != 0 else 4
        elif x == 4:
            move.forward()
            time.sleep(1)
            while ir.get_value() > threshold[0]:
                move.left()
            move.stop()
            fix()
            motor.servoMB()
            move.forward()
            time.sleep(0.5)
            motor.servoMA()
            x += 1
        elif x == 5:
            pick()
            move.backward()
            time.sleep(0.5)
            while ir.get_value() > threshold[0]:
                move.left()
            move.stop()
            fix()
            move.forward()
            time.sleep(0.5)
            x += 1
        elif x == 6:
            move.forward()
            time.sleep(0.5)
            while ir.get_value() > threshold[0]:
                move.left()
            move.stop()
            fix()
            event.move()()
            time.sleep(0.5)
            x, y = 3, 1
        elif x == 7:
            return move.stop()

    # elif times >= 2:
    #     move.forward()
    #     time.sleep(0.5)
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
    else:
        fix()
        event.move()()

# if __name__ == "__main__":
setup()
move.forward()
while True:
    tracking()