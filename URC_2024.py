from pyatcrobo2.parts import Servomotor, IRPhotoReflector, DCMotor
from pystubit.board import button_a, display
import time

class IRSensor:
    def __init__(self, port, threshold=2000) -> None:
        self.sensor = IRPhotoReflector(port)
        self.threshold = threshold

    def get_value(self) -> int:
        return self.sensor.get_value()

    def set_threshold(self, threshold) -> None:
        self.threshold = threshold

    def is_black(self) -> bool:
        value = self.get_value()
        return True if value < self.threshold else False


class CarMotor:
    def __init__(self, port, power=100) -> None:
        self.motor = DCMotor(port)
        self.power = power

    def set_power(self, power) -> None:
        self.power = power

    def forward(self) -> None:
        self.motor.power(self.power)
        self.motor.ccw()

    def backward(self) -> None:
        self.motor.power(self.power)
        self.motor.cw()

    def stop(self):
        self.motor.brake()


class ServoMotor:
    def __init__(self, port) -> None:
        self.servo = Servomotor(port)
        self.angle = 60

    def set_angle(self, angle) -> None:
        self.angle = angle
        self.servo.set_angle(angle)


ir_left = IRSensor('P0')
ir_right = IRSensor('P1')
ir_center = IRSensor('P2')

motor_left = CarMotor('M2')
motor_right = CarMotor('M1')

servo1 = ServoMotor('P15')
servo2 = ServoMotor('P13')
servo3 = ServoMotor('P14')


def set_power(left, right=None):
    right = left if not right else right
    motor_left.set_power(left)
    motor_right.set_power(right)


def move_forward():
    motor_left.forward()
    motor_right.forward()


def move_backward():
    motor_left.backward()
    motor_right.backward()


def turn_left():
    motor_right.forward()
    motor_left.backward()


def turn_right():
    motor_left.forward()
    motor_right.backward()


def stop():
    motor_left.stop()
    motor_right.stop()


def auto_left():
    turn_left()
    while ir_right.is_black():
        pass
    while not ir_right.is_black():
        pass
    stop()


def auto_right():
    turn_right()
    while ir_left.is_black():
        pass
    while not ir_left.is_black():
        pass
    stop()


def pick(angle, sleep=None):
    for i, r in zip(range(servo2.angle, angle, 1 if servo2.angle < angle else -1),
                    range(servo3.angle, angle, 1 if servo3.angle < angle else -1)):
        servo3.set_angle(r)
        servo2.set_angle(i)
        if sleep:
            time.sleep(sleep)

def drop(angle=60):
    for i, r in zip(range(servo2.angle, angle, -1 if servo2.angle > angle else 1),
                    range(servo3.angle, angle, -1 if servo3.angle > angle else 1)):
        servo3.set_angle(r)
        servo2.set_angle(i)

def set_hight(hight, sleep=None):
    for i in range(servo1.angle, hight, 1 if servo1.angle < hight else -1):
        servo1.set_angle(hight)
        if sleep:
            time.sleep(sleep)

def fix(event=stop):
    while ir_left.is_black() or ir_right.is_black():
        if ir_left.is_black() and not ir_right.is_black():
            turn_right()
        elif ir_right.is_black() and not ir_left.is_black():
            turn_left()
        else:
            break  
    event()


def forward_line(move, times=1):
    move()
    for _ in range(times):
        while ir_left.is_black() and ir_right.is_black():
            pass
        while True:
            if ir_left.is_black() and ir_right.is_black():
                break
            else:
                if move != move_backward:
                    fix(move)
    stop()


def square():
    forward_line(move_forward, 3)
    auto_left()
    while True:
        move_forward()
        forward_line(move_forward, 2)
        auto_left()


def setup(threshold='auto'):
    temp = []
    if not threshold:
        for i in range(2):
            while button_a.is_pressed():
                pass
            display.show("W" if i == 0 else "B", delay=0)
            while not button_a.is_pressed():

                pass
            temp += [ir_left.get_value(), ir_right.get_value()]
        while button_a.is_pressed():
            pass
        ir_left.set_threshold(int((temp[0] + temp[2]) / 2))
        ir_right.set_threshold(int((temp[1] + temp[3]) / 2))
    elif threshold == 'auto':
        display.show("Auto", delay=0)
        while button_a.is_pressed():
            pass
        while not button_a.is_pressed():
            pass
        # if not ir_left.get_value() >= ir_left.threshold or not ir_right.get_value() >= ir_right.threshold:
        #     move_forward()
        #     while not ir_left.get_value() >= ir_left.threshold or not ir_right.get_value() >= ir_right.threshold:
        #         pass
        #     stop()
        temp += [ir_left.get_value(), ir_right.get_value()]
        for index, ir in enumerate([ir_left, ir_right]):
            if temp[index] - ir.get_value() <= 1000:
                move_forward()
                while temp[index] - ir.get_value() <= 1000:
                    pass
            stop()
            temp += [ir.get_value()]
        ir_left.set_threshold(int((temp[0] + temp[2]) / 2))
        ir_right.set_threshold(int((temp[1] + temp[3]) / 2))
    elif isinstance(threshold, list):
        ir_left.set_threshold(threshold[0])
        ir_right.set_threshold(threshold[1])
    display.show("G", delay=0)
    while not button_a.is_pressed():
        pass
    display.clear()
    servo1.set_angle(0)
    servo2.set_angle(60)
    servo3.set_angle(60)

setup()
# Part 1
pick(55)
forward_line(move_forward, 3)
move_forward()
time.sleep(0.5)
stop()
time.sleep(0.5)
pick(100, 0.05)
time.sleep(0.5)
forward_line(move_backward, 2)
move_backward()
time.sleep(0.46)
stop()
drop()

# Part 2
time.sleep(0.5)
set_power(150)
forward_line(move_backward)
move_backward()
time.sleep(1.3)
turn_right()
time.sleep(0.6)
move_forward()
time.sleep(0.5)
while not ir_left.is_black() or not ir_right.is_black():
    pass
move_forward()
time.sleep(0.5)
auto_left()
set_power(100)
forward_line(move_forward, 2)
set_power(100)
move_forward()
time.sleep(0.3)
while ir_center.get_value() >= 380:
    move_backward()
    fix()
time.sleep(0.5)
pick(100, 0.05)
set_power(80)
time.sleep(0.5)
set_hight(85)
time.sleep(0.5)
while ir_center.get_value() <= 340:
    move_forward()
    fix()
time.sleep(0.5)
set_hight(77)
time.sleep(0.5)
pick(100)
time.sleep(0.5)
drop()
time.sleep(0.5)
set_hight(0)
set_power(75)
time.sleep(0.5)
forward_line(move_forward)
set_power(100)
time.sleep(0.5)
move_backward()
time.sleep(0.35)
stop()
time.sleep(0.5)
pick(100, 0.05)
time.sleep(0.5)
forward_line(move_backward)
set_power(70)
move_forward()
time.sleep(2)
turn_left()
time.sleep(0.5)
move_backward()
time.sleep(1)
turn_left()
time.sleep(1.5)
stop()
time.sleep(0.5)
pick(0)
for i in range(7):
    move_forward()
    time.sleep(0.1)
stop()
move_forward()
time.sleep(0.5)
forward_line(move_backward)

#part 3
set_hight(130)
time.sleep(0.5)
move_forward()
time.sleep(0.5)
auto_left()
forward_line(move_forward)
set_power(100)
set_hight(0)
drop()
time.sleep(0.5)
move_forward()
time.sleep(3.5)
turn_right()
time.sleep(1)
move_forward()
time.sleep(0.5)
while not ir_left.is_black() or not ir_right.is_black():
    pass
time.sleep(0.5)
while not  ir_left.is_black() or not ir_right.is_black():
    pass
move_forward()
time.sleep(0.5)
auto_right ()
forward_line(move_forward, 2)
# >>>
move_forward()
time.sleep(0.3) 
while ir_center.get_value() >= 380:
    move_backward()
    fix()
time.sleep(0.5)
pick(100, 0.05)
time.sleep(0.5)
set_hight(95)
time.sleep(0.5)
while ir_center.get_value() <= 340:
    move_forward()
    fix()
time.sleep(0.5)
set_hight(77)
time.sleep(0.5)
pick(100)
time.sleep(0.5)
drop()
time.sleep(0.5)
set_hight(0)
time.sleep(0.5)
forward_line(move_forward)
time.sleep(0.5)
move_backward()
time.sleep(0.35)
stop()
time.sleep(0.5)  
pick(100, 0.05)
time.sleep(0.3)
move_backward()
time.sleep(0.5)
forward_line(move_backward)
move_backward()
time.sleep(0.5)
set_hight(130)
time.sleep(0.5)
turn_right()
time.sleep(0.80)
stop()
time.sleep(0.5)
for i in range(11):
    move_forward()
    time.sleep(0.1)
stop()
time.sleep(0.5)
set_hight(125)
time.sleep(0.5)
pick(85)
time.sleep(0.5)
set_hight(140)
time.sleep(0.5)
move_backward()
time.sleep(0.8)
stop()
